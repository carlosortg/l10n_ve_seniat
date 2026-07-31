# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_ve_control_number = fields.Char(
        string="Numero de control",
        copy=False,
        tracking=True,
        help="Numero de control correlativo SENIAT (sin huecos).",
    )
    l10n_ve_invoice_number = fields.Char(string="Numero de factura fiscal", copy=False)
    l10n_ve_origin_move_id = fields.Many2one(
        "account.move",
        string="Documento origen (NC/ND)",
        copy=False,
        help="Factura que corrige esta nota de credito/debito.",
    )

    def _l10n_ve_assign_control_number(self):
        for move in self:
            if move.move_type not in ("out_invoice", "out_refund") or move.l10n_ve_control_number:
                continue
            seq = move.company_id.l10n_ve_control_number_sequence_id
            if not seq:
                seq = self.env["ir.sequence"].search([
                    ("code", "=", "l10n.ve.control.number"),
                    ("company_id", "in", [move.company_id.id, False]),
                ], limit=1)
            if seq:
                move.l10n_ve_control_number = seq.next_by_id()

    def action_post(self):
        res = super().action_post()
        self._l10n_ve_assign_control_number()
        return res
