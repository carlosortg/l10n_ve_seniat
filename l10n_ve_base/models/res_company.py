# -*- coding: utf-8 -*-
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_ve_rif = fields.Char(
        string="RIF de la Compañía",
        related="partner_id.l10n_ve_rif",
        readonly=False,
        store=True,
    )
    l10n_ve_taxpayer_type = fields.Selection(
        related="partner_id.l10n_ve_taxpayer_type",
        readonly=False,
        store=True,
        string="Tipo de Contribuyente",
    )
    l10n_ve_is_retention_agent = fields.Boolean(
        related="partner_id.l10n_ve_is_retention_agent",
        readonly=False,
        store=True,
        string="Es Agente de Retención",
    )
    l10n_ve_economic_activity = fields.Char(
        related="partner_id.l10n_ve_economic_activity",
        readonly=False,
        store=True,
        string="Actividad Económica",
    )
    l10n_ve_control_number_sequence_id = fields.Many2one(
        "ir.sequence",
        string="Secuencia Número de Control",
        copy=False,
    )
    l10n_ve_invoice_authorization = fields.Char(
        string="Autorización / Resolución de Facturación",
        help="Número de resolución o autorización de facturación otorgada por el SENIAT (si aplica).",
    )
