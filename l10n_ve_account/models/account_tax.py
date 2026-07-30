# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    l10n_ve_withholding_type = fields.Selection(
        selection=[
            ("none", "No aplica retencion"),
            ("iva", "Retencion IVA"),
            ("islr", "Retencion ISLR"),
        ],
        string="Tipo retencion VE",
        default="none",
    )
    l10n_ve_iva_aliquot = fields.Selection(
        selection=[
            ("general", "General 16%"),
            ("reduced", "Reducida 8%"),
            ("additional", "Adicional 31%"),
            ("exempt", "Exento 0%"),
        ],
        string="Alicuota IVA VE",
    )
