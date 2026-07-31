# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_ve_bcv_auto_fetch = fields.Boolean(related="company_id.l10n_ve_bcv_auto_fetch", readonly=False)
    l10n_ve_bcv_rate_url = fields.Char(related="company_id.l10n_ve_bcv_rate_url", readonly=False)
