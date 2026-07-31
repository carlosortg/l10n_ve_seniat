# -*- coding: utf-8 -*-
from odoo import fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"

    l10n_ve_lock_control_number = fields.Boolean(
        string="Bloquear documentos con N de control",
        default=True,
        help="Impide volver a borrador facturas ya numeradas (inalterabilidad).",
    )
    l10n_ve_require_nc_origin = fields.Boolean(
        string="NC exige documento origen",
        default=True,
    )

    def action_create_seniat_sequences(self):
        Sequence = self.env["ir.sequence"]
        for company in self:
            if not company.l10n_ve_control_number_sequence_id:
                seq = Sequence.create({
                    "name": _("N control SENIAT - %s") % company.name,
                    "code": "l10n.ve.control.number",
                    "prefix": "",
                    "padding": 8,
                    "implementation": "no_gap",
                    "company_id": company.id,
                })
                company.l10n_ve_control_number_sequence_id = seq.id
            # Secuencia comprobantes retencion por si no existen
            for code, label, prefix in [
                ("l10n.ve.withholding.iva", "Retencion IVA", "RET-IVA/%(year)s/"),
                ("l10n.ve.withholding.islr", "Retencion ISLR", "RET-ISLR/%(year)s/"),
            ]:
                exists = Sequence.search([
                    ("code", "=", code),
                    ("company_id", "in", [company.id, False]),
                ], limit=1)
                if not exists:
                    Sequence.create({
                        "name": _("%s - %s") % (label, company.name),
                        "code": code,
                        "prefix": prefix,
                        "padding": 6,
                        "implementation": "no_gap",
                        "company_id": company.id,
                    })
        return {
            "type": "ir.actions.client",
            "tag": "display_notification",
            "params": {
                "title": _("Secuencias SENIAT"),
                "message": _("Secuencias creadas o ya existentes."),
                "type": "success",
                "sticky": False,
            },
        }
