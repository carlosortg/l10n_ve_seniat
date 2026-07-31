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
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    partner_id = fields.Many2one("res.partner", string="Sujeto retenido", required=True, tracking=True)
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
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id", store=True)
    amount_base = fields.Monetary(currency_field="currency_id", string="Base imponible")
    amount_withheld = fields.Monetary(currency_field="currency_id", string="Monto retenido")
    rate = fields.Float(string="Porcentaje %", digits=(16, 4))
    invoice_ids = fields.Many2many(
        "account.move",
        "account_withholding_invoice_rel",
        "withholding_id",
        "invoice_id",
        string="Facturas",
    )
    line_ids = fields.One2many("account.withholding.line", "withholding_id", string="Lineas")
    notes = fields.Text()
    move_id = fields.Many2one("account.move", string="Asiento contable", readonly=True, copy=False)

    def action_confirm(self):
        for rec in self:
            if rec.state != "draft":
                continue
            if not rec.amount_withheld:
                raise UserError(_("Indique el monto retenido."))
            seq_code = "l10n.ve.withholding.iva" if rec.withholding_type == "iva" else "l10n.ve.withholding.islr"
            if rec.name in (False, "/"):
                rec.name = self.env["ir.sequence"].next_by_code(seq_code) or "/"
            rec.state = "confirmed"

    def action_declare(self):
        self.filtered(lambda r: r.state == "confirmed").write({"state": "declared"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_draft(self):
        self.filtered(lambda r: r.state == "cancelled").write({"state": "draft"})


class AccountWithholdingLine(models.Model):
    _name = "account.withholding.line"
    _description = "Linea de retencion VE"

    withholding_id = fields.Many2one("account.withholding", required=True, ondelete="cascade")
    invoice_id = fields.Many2one("account.move", string="Factura")
    currency_id = fields.Many2one(related="withholding_id.currency_id")
    amount_base = fields.Monetary(currency_field="currency_id")
    amount_withheld = fields.Monetary(currency_field="currency_id")
    rate = fields.Float(string="%")
