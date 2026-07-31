# -*- coding: utf-8 -*-
from odoo import fields, models


class ResBank(models.Model):
    _inherit = "res.bank"

    l10n_ve_bank_code = fields.Char(string="Codigo banco VE", index=True)
    l10n_ve_is_local = fields.Boolean(string="Banco local Venezuela", default=False)
