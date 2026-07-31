# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_ve_bcv_auto_fetch = fields.Boolean(string="Actualizar tasa BCV automaticamente")
    l10n_ve_bcv_rate_url = fields.Char(string="URL fuente BCV", default="https://www.bcv.org.ve/")
