# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    def action_create_seniat_sequences(self):
        Sequence = self.env["ir.sequence"]
        for company in self:
            if not company.l10n_ve_control_number_sequence_id:
                seq = Sequence.create({
                    "name": "N control SENIAT - %s" % company.name,
                    "code": "l10n.ve.control.number",
                    "prefix": "",
                    "padding": 8,
                    "implementation": "no_gap",
                    "company_id": company.id,
                })
                company.l10n_ve_control_number_sequence_id = seq.id
        return True
