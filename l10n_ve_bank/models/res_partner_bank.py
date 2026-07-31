# -*- coding: utf-8 -*-
from odoo import fields, models


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    l10n_ve_account_type = fields.Selection(
        selection=[
            ("checking", "Cuenta corriente"),
            ("savings", "Cuenta de ahorro"),
            ("payroll", "Cuenta nomina"),
            ("other", "Otra"),
        ],
        string="Tipo de cuenta VE",
        default="checking",
    )
    l10n_ve_holder_id = fields.Char(string="Cedula / RIF del titular")
    l10n_ve_phone_sms = fields.Char(string="Telefono Pago Movil")
