# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_ve_iva_withholding_rate = fields.Selection(
        selection=[("75", "75%"), ("100", "100%")],
        string="% retencion IVA sugerido",
        help="Usado al generar retenciones desde la factura.",
    )
