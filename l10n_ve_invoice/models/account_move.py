# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_ve_control_number = fields.Char(
        string="Numero de control",
        copy=False,
        tracking=True,
        index=True,
        help="Numero de control correlativo SENIAT (implementation=no_gap).",
    )
    l10n_ve_invoice_number = fields.Char(
        string="Numero de factura fiscal",
        copy=False,
        tracking=True,
        help="Numero fiscal impreso si difiere del name de Odoo.",
    )
    l10n_ve_origin_move_id = fields.Many2one(
        "account.move",
        string="Documento origen",
        copy=False,
        tracking=True,
        domain="[('move_type', 'in', ('out_invoice', 'in_invoice')), ('state', '=', 'posted'), ('partner_id', '=', partner_id)]",
        help="Factura que corrige esta nota de credito o debito.",
    )
    l10n_ve_document_type = fields.Selection(
        selection=[
            ("invoice", "Factura"),
            ("credit_note", "Nota de credito"),
            ("debit_note", "Nota de debito"),
        ],
        string="Tipo documento fiscal",
        compute="_compute_l10n_ve_document_type",
        store=True,
    )
    l10n_ve_requires_control = fields.Boolean(
        compute="_compute_l10n_ve_requires_control",
    )

    @api.depends("move_type", "debit_origin_id")
    def _compute_l10n_ve_document_type(self):
        for move in self:
            if move.move_type in ("out_refund", "in_refund"):
                move.l10n_ve_document_type = "credit_note"
            elif move.move_type in ("out_invoice", "in_invoice") and move.debit_origin_id:
                move.l10n_ve_document_type = "debit_note"
            elif move.move_type in ("out_invoice", "in_invoice"):
                move.l10n_ve_document_type = "invoice"
            else:
                move.l10n_ve_document_type = False

    @api.depends("move_type", "company_id", "journal_id")
    def _compute_l10n_ve_requires_control(self):
        for move in self:
            # Ventas (y opcionalmente compras si el diario lo exige)
            sale = move.move_type in ("out_invoice", "out_refund")
            journal_flag = bool(move.journal_id.l10n_ve_require_control_number)
            move.l10n_ve_requires_control = sale or journal_flag

    def _l10n_ve_get_control_sequence(self):
        self.ensure_one()
        seq = self.journal_id.l10n_ve_control_sequence_id
        if not seq:
            seq = self.company_id.l10n_ve_control_number_sequence_id
        if not seq:
            seq = self.env["ir.sequence"].search([
                ("code", "=", "l10n.ve.control.number"),
                ("company_id", "in", [self.company_id.id, False]),
            ], limit=1)
        return seq

    def _l10n_ve_assign_control_number(self):
        for move in self:
            if not move.l10n_ve_requires_control:
                continue
            if move.l10n_ve_control_number:
                continue
            if move.state != "posted":
                continue
            seq = move._l10n_ve_get_control_sequence()
            if not seq:
                raise UserError(_(
                    "No hay secuencia de Numero de Control SENIAT configurada.\n"
                    "Vaya a Compania -> SENIAT -> Crear secuencias, "
                    "o asigne una secuencia en el diario %s."
                ) % (move.journal_id.display_name,))
            move.l10n_ve_control_number = seq.next_by_id()
            if not move.l10n_ve_invoice_number and move.name and move.name != "/":
                move.l10n_ve_invoice_number = move.name

    def _l10n_ve_check_partner_rif(self):
        for move in self:
            if move.move_type not in ("out_invoice", "out_refund", "in_invoice", "in_refund"):
                continue
            partner = move.partner_id.commercial_partner_id
            country = partner.country_id or move.company_id.country_id
            if country and country.code != "VE":
                continue
            if not (partner.l10n_ve_rif or partner.vat):
                raise UserError(_(
                    "El contacto %s no tiene RIF/VAT. "
                    "Es obligatorio para documentos fiscales en Venezuela."
                ) % partner.display_name)

    def _l10n_ve_check_credit_note_origin(self):
        for move in self:
            if move.move_type in ("out_refund", "in_refund") and move.company_id.l10n_ve_require_nc_origin:
                if not move.l10n_ve_origin_move_id and not move.reversed_entry_id:
                    raise UserError(_(
                        "La nota de credito debe indicar el documento origen "
                        "(campo Documento origen o factura revertida)."
                    ))

    def action_post(self):
        self._l10n_ve_check_partner_rif()
        self._l10n_ve_check_credit_note_origin()
        res = super().action_post()
        self._l10n_ve_assign_control_number()
        return res

    def button_draft(self):
        for move in self:
            if move.l10n_ve_control_number and move.company_id.l10n_ve_lock_control_number:
                raise UserError(_(
                    "No se puede volver a borrador el documento %s: "
                    "tiene Numero de Control %s y la compania bloquea su alteracion."
                ) % (move.name, move.l10n_ve_control_number))
        return super().button_draft()

    def unlink(self):
        for move in self:
            if move.l10n_ve_control_number and move.state == "posted":
                raise UserError(_(
                    "No se puede eliminar un documento publicado con Numero de Control (%s)."
                ) % move.l10n_ve_control_number)
        return super().unlink()
