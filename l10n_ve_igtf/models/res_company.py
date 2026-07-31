# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_ve_igtf_rate = fields.Float(string="Porcentaje IGTF %", default=3.0)
    l10n_ve_igtf_account_id = fields.Many2one("account.account", string="Cuenta IGTF")
