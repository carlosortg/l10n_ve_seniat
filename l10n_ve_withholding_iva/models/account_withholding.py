# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountWithholding(models.Model):
    _inherit = "account.withholding"

    l10n_ve_iva_retention_rate = fields.Selection(
        selection=[("75", "75%"), ("100", "100%")],
        string="Tasa retencion IVA",
        default="75",
    )

    @api.onchange("l10n_ve_iva_retention_rate", "amount_base", "withholding_type")
    def _onchange_iva_rate(self):
        for rec in self:
            if rec.withholding_type == "iva" and rec.amount_base:
                pct = float(rec.l10n_ve_iva_retention_rate or 75)
                # Retencion sobre el IVA, no sobre la base: el usuario suele cargar amount_base = IVA
                rec.rate = pct
                rec.amount_withheld = rec.amount_base * pct / 100.0
