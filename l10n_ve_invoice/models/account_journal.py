# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    l10n_ve_control_sequence_id = fields.Many2one(
        "ir.sequence",
        string="Secuencia N control VE",
        help="Si se define, se usa en lugar de la secuencia de compania.",
    )
