# -*- coding: utf-8 -*-
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    l10n_ve_control_number_sequence_id = fields.Many2one(
        related="company_id.l10n_ve_control_number_sequence_id",
        readonly=False,
    )
    l10n_ve_lock_control_number = fields.Boolean(
        related="company_id.l10n_ve_lock_control_number",
        readonly=False,
    )
    l10n_ve_require_nc_origin = fields.Boolean(
        related="company_id.l10n_ve_require_nc_origin",
        readonly=False,
    )
