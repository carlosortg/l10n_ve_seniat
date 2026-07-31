# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    l10n_ve_payment_reference = fields.Char(string="Referencia bancaria VE", copy=False)
    l10n_ve_payment_channel = fields.Selection(
        selection=[
            ("transfer", "Transferencia"),
            ("mobile", "Pago movil"),
            ("deposit", "Deposito"),
            ("check", "Cheque"),
            ("cash", "Efectivo"),
            ("other", "Otro"),
        ],
        string="Canal de pago VE",
        default="transfer",
    )
