# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    l10n_ve_payment_reference = fields.Char(string="Referencia bancaria VE", copy=False, tracking=True)
    l10n_ve_payment_channel = fields.Selection(
        selection=[
            ("transfer", "Transferencia"),
            ("mobile", "Pago móvil"),
            ("deposit", "Depósito"),
            ("check", "Cheque"),
            ("cash", "Efectivo"),
            ("pos", "Punto de venta"),
            ("other", "Otro"),
        ],
        string="Canal de pago VE",
        default="transfer",
    )
    l10n_ve_bank_concept = fields.Char(string="Concepto bancario")
