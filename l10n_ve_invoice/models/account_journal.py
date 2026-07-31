# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "account.journal"

    l10n_ve_control_sequence_id = fields.Many2one(
        "ir.sequence",
        string="Secuencia N control VE",
        help="Si se define, se usa en lugar de la secuencia de la compania.",
        check_company=True,
    )
    l10n_ve_require_control_number = fields.Boolean(
        string="Exigir N de control",
        help="Asigna y exige numero de control al publicar (ademas de diarios de venta).",
    )
    l10n_ve_is_fiscal = fields.Boolean(
        string="Diario fiscal VE",
        help="Marca el diario como de facturacion fiscal SENIAT.",
    )
