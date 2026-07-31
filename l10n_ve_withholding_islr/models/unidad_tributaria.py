# -*- coding: utf-8 -*-
from odoo import fields, models


class L10nVeUnidadTributaria(models.Model):
    _name = "l10n.ve.unidad.tributaria"
    _description = "Unidad Tributaria"
    _order = "date_from desc"

    name = fields.Char(required=True)
    amount = fields.Float(string="Valor UT", required=True, digits=(16, 4))
    date_from = fields.Date(required=True)
    date_to = fields.Date()
    active = fields.Boolean(default=True)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company)
