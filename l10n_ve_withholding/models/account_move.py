# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_ve_withholding_ids = fields.Many2many(
        "account.withholding",
        "account_withholding_invoice_rel",
        "invoice_id",
        "withholding_id",
        string="Retenciones",
        copy=False,
    )
    l10n_ve_withholding_count = fields.Integer(compute="_compute_l10n_ve_withholding_count")
    l10n_ve_suffered_iva = fields.Monetary(string="Retencion IVA sufrida", currency_field="currency_id", copy=False)
    l10n_ve_suffered_islr = fields.Monetary(string="Retencion ISLR sufrida", currency_field="currency_id", copy=False)
    l10n_ve_suffered_voucher = fields.Char(string="N comprobante retencion sufrida", copy=False)
    l10n_ve_suffered_move_id = fields.Many2one("account.move", string="Asiento retencion sufrida", copy=False, readonly=True)

    def _compute_l10n_ve_withholding_count(self):
        for move in self:
            move.l10n_ve_withholding_count = len(move.l10n_ve_withholding_ids)

    def action_view_withholdings(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Retenciones"),
            "res_model": "account.withholding",
            "view_mode": "list,form",
            "domain": [("id", "in", self.l10n_ve_withholding_ids.ids)],
        }
