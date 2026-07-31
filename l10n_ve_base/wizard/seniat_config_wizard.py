# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class L10nVeSeniatConfigWizard(models.TransientModel):
    _name = "l10n.ve.seniat.config.wizard"
    _description = "Asistente de configuracion inicial SENIAT"

    state = fields.Selection(
        selection=[
            ("company", "1. Compania"),
            ("sequences", "2. Secuencias"),
            ("accounts", "3. Cuentas"),
            ("done", "Listo"),
        ],
        default="company",
    )
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)
    l10n_ve_rif = fields.Char(string="RIF de la empresa")
    l10n_ve_taxpayer_type = fields.Selection(
        selection=[
            ("ordinary", "Contribuyente Ordinario"),
            ("special", "Contribuyente Especial"),
            ("formal", "Contribuyente Formal"),
            ("public", "Ente Publico"),
        ],
        string="Tipo de contribuyente",
        default="ordinary",
    )
    l10n_ve_is_retention_agent = fields.Boolean(string="Es agente de retencion")
    create_sequences = fields.Boolean(string="Crear secuencias SENIAT", default=True)
    note = fields.Html(default=lambda self: _("<p>Configura RIF, tipo de contribuyente y secuencias SENIAT.</p>"))

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        company = self.env.company
        res["l10n_ve_rif"] = company.l10n_ve_rif or company.vat or ""
        res["l10n_ve_taxpayer_type"] = company.l10n_ve_taxpayer_type or "ordinary"
        res["l10n_ve_is_retention_agent"] = company.l10n_ve_is_retention_agent
        return res

    def action_next(self):
        self.ensure_one()
        if self.state == "company":
            company = self.company_id
            company.write({
                "l10n_ve_rif": self.l10n_ve_rif,
                "l10n_ve_taxpayer_type": self.l10n_ve_taxpayer_type,
                "l10n_ve_is_retention_agent": self.l10n_ve_is_retention_agent,
            })
            if self.l10n_ve_rif and company.partner_id:
                company.partner_id.write({
                    "l10n_ve_rif": self.l10n_ve_rif,
                    "l10n_ve_taxpayer_type": self.l10n_ve_taxpayer_type,
                    "l10n_ve_is_retention_agent": self.l10n_ve_is_retention_agent,
                })
            self.state = "sequences"
        elif self.state == "sequences":
            if self.create_sequences and hasattr(self.company_id, "action_create_seniat_sequences"):
                self.company_id.action_create_seniat_sequences()
            self.state = "accounts"
        elif self.state == "accounts":
            self.state = "done"
        return self._reopen()

    def action_back(self):
        order = ["company", "sequences", "accounts", "done"]
        idx = order.index(self.state)
        if idx > 0:
            self.state = order[idx - 1]
        return self._reopen()

    def _reopen(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "l10n.ve.seniat.config.wizard",
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }

    def action_close(self):
        return {"type": "ir.actions.act_window_close"}
