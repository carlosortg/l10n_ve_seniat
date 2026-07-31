# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountWithholding(models.Model):
    _name = "account.withholding"
    _description = "Comprobante de retencion VE"
    _order = "date desc, id desc"
    _inherit = ["mail.thread", "mail.activity.mixin"]

    name = fields.Char(string="Numero", readonly=True, copy=False, default="/")
    date = fields.Date(required=True, default=fields.Date.context_today, tracking=True)
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company, index=True,
    )
    currency_id = fields.Many2one(related="company_id.currency_id", store=True)
    partner_id = fields.Many2one(
        "res.partner", string="Sujeto retenido", required=True, tracking=True,
        domain="[('company_id', 'in', (False, company_id))]",
    )
    partner_rif = fields.Char(related="partner_id.l10n_ve_rif", string="RIF sujeto")
    withholding_type = fields.Selection(
        selection=[("iva", "IVA"), ("islr", "ISLR"), ("other", "Otro")],
        required=True,
        default="iva",
        tracking=True,
    )
    state = fields.Selection(
        selection=[
            ("draft", "Borrador"),
            ("confirmed", "Confirmado"),
            ("declared", "Declarado"),
            ("cancelled", "Anulado"),
        ],
        default="draft",
        tracking=True,
        copy=False,
    )
    amount_base = fields.Monetary(currency_field="currency_id", string="Base / IVA retenible", tracking=True)
    amount_withheld = fields.Monetary(currency_field="currency_id", string="Monto retenido", tracking=True)
    rate = fields.Float(string="Porcentaje %", digits=(16, 4))
    invoice_ids = fields.Many2many(
        "account.move",
        "account_withholding_invoice_rel",
        "withholding_id",
        "invoice_id",
        string="Facturas",
        domain="[('partner_id', '=', partner_id), ('state', '=', 'posted')]",
    )
    line_ids = fields.One2many("account.withholding.line", "withholding_id", string="Lineas")
    notes = fields.Text()
    move_id = fields.Many2one("account.move", string="Asiento contable", readonly=True, copy=False)
    journal_id = fields.Many2one(
        "account.journal",
        string="Diario",
        domain="[('type', '=', 'general'), ('company_id', '=', company_id)]",
        check_company=True,
    )

    @api.onchange("line_ids")
    def _onchange_lines(self):
        for rec in self:
            rec.amount_base = sum(rec.line_ids.mapped("amount_base"))
            rec.amount_withheld = sum(rec.line_ids.mapped("amount_withheld"))

    def action_confirm(self):
        for rec in self:
            if rec.state != "draft":
                continue
            if not rec.amount_withheld:
                raise UserError(_("Indique el monto retenido."))
            if not rec.partner_id:
                raise UserError(_("Indique el sujeto retenido."))
            seq_code = (
                "l10n.ve.withholding.iva"
                if rec.withholding_type == "iva"
                else "l10n.ve.withholding.islr"
            )
            if rec.name in (False, "/"):
                rec.name = self.env["ir.sequence"].with_company(rec.company_id).next_by_code(seq_code) or "/"
            if not rec.move_id:
                rec._l10n_ve_create_account_move()
            rec.state = "confirmed"

    def _l10n_ve_create_account_move(self):
        """Asiento: Dr retencion por pagar / Cr cuenta por pagar proveedor (simplificado)."""
        self.ensure_one()
        company = self.company_id
        journal = self.journal_id or self.env["account.journal"].search([
            ("type", "=", "general"),
            ("company_id", "=", company.id),
        ], limit=1)
        if not journal:
            raise UserError(_("Configure un diario de operaciones varias (general) para retenciones."))

        account_wh = company.l10n_ve_iva_withholding_account_id if self.withholding_type == "iva" else company.l10n_ve_islr_withholding_account_id
        if not account_wh:
            # Intentar cuenta por codigo tipico o omitir asiento con aviso
            raise UserError(_(
                "Configure la cuenta de retencion IVA/ISLR en la compania "
                "(campo Cuenta retencion IVA / ISLR)."
            ))

        # Contrapartida: cuenta por pagar del partner si existe
        payable = self.partner_id.property_account_payable_id
        if not payable:
            raise UserError(_("El proveedor no tiene cuenta por pagar configurada."))

        move_vals = {
            "ref": self.name,
            "date": self.date,
            "journal_id": journal.id,
            "company_id": company.id,
            "partner_id": self.partner_id.id,
            "line_ids": [
                (0, 0, {
                    "name": _("Retencion %s %s") % (self.withholding_type.upper(), self.name),
                    "account_id": account_wh.id,
                    "partner_id": self.partner_id.id,
                    "debit": self.amount_withheld,
                    "credit": 0.0,
                }),
                (0, 0, {
                    "name": _("Retencion %s %s") % (self.withholding_type.upper(), self.name),
                    "account_id": payable.id,
                    "partner_id": self.partner_id.id,
                    "debit": 0.0,
                    "credit": self.amount_withheld,
                }),
            ],
        }
        move = self.env["account.move"].create(move_vals)
        move.action_post()
        self.move_id = move.id

    def action_declare(self):
        self.filtered(lambda r: r.state == "confirmed").write({"state": "declared"})

    def action_cancel(self):
        for rec in self:
            if rec.move_id and rec.move_id.state == "posted":
                rec.move_id.button_draft()
                rec.move_id.button_cancel()
            rec.state = "cancelled"

    def action_draft(self):
        self.filtered(lambda r: r.state == "cancelled").write({"state": "draft", "move_id": False})


class AccountWithholdingLine(models.Model):
    _name = "account.withholding.line"
    _description = "Linea de retencion VE"

    withholding_id = fields.Many2one("account.withholding", required=True, ondelete="cascade")
    invoice_id = fields.Many2one("account.move", string="Factura")
    currency_id = fields.Many2one(related="withholding_id.currency_id")
    amount_base = fields.Monetary(currency_field="currency_id")
    amount_withheld = fields.Monetary(currency_field="currency_id")
    rate = fields.Float(string="%")
    invoice_control_number = fields.Char(
        related="invoice_id.l10n_ve_control_number", string="N control factura",
    )
