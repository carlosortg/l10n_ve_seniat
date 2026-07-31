# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_ve_iva_withholding_account_id = fields.Many2one("account.account", string="Cuenta retencion IVA")
    l10n_ve_islr_withholding_account_id = fields.Many2one("account.account", string="Cuenta retencion ISLR")
