# -*- coding: utf-8 -*-
from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    l10n_ve_igtf_amount = fields.Monetary(
        string="IGTF",
        currency_field="currency_id",
        compute="_compute_l10n_ve_igtf",
        store=True,
        readonly=False,
    )
    l10n_ve_apply_igtf = fields.Boolean(
        string="Aplicar IGTF",
        help="Marcar si el pago en divisa genera IGTF.",
    )

    @api.depends("amount", "currency_id", "company_id", "l10n_ve_apply_igtf")
    def _compute_l10n_ve_igtf(self):
        for pay in self:
            rate = pay.company_id.l10n_ve_igtf_rate or 3.0
            company_cur = pay.company_id.currency_id
            if pay.l10n_ve_apply_igtf and pay.currency_id and pay.currency_id != company_cur:
                pay.l10n_ve_igtf_amount = pay.amount * rate / 100.0
            else:
                pay.l10n_ve_igtf_amount = 0.0
