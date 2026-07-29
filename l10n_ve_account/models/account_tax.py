# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountTax(models.Model):
    _inherit = "account.tax"

    l10n_ve_withholding_type = fields.Selection(
        selection=[
            ("none", "No es retención"),
            ("iva", "Retención de IVA"),
            ("islr", "Retención de ISLR"),
            ("municipal", "Retención Municipal"),
            ("igtf", "IGTF"),
        ],
        string="Tipo de Retención VE",
        default="none",
    )
    l10n_ve_aliquot = fields.Selection(
        selection=[
            ("general", "General 16%"),
            ("reduced", "Reducida 8%"),
            ("luxury", "Lujo 31%"),
            ("exempt", "Exento 0%"),
            ("export", "Exportación 0%"),
            ("not_subject", "No sujeto"),
        ],
        string="Alícuota IVA VE",
    )
