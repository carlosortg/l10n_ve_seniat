# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class L10nVeBcvRate(models.Model):
    _name = "l10n.ve.bcv.rate"
    _description = "Tasa BCV"
    _order = "date desc, id desc"

    date = fields.Date(required=True, default=fields.Date.context_today, index=True)
    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        default=lambda self: self.env.ref("base.USD", raise_if_not_found=False),
    )
    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    rate = fields.Float(string="VES por 1 unidad", digits=(16, 8), required=True)
    source = fields.Selection(
        [("manual", "Manual"), ("bcv_web", "BCV web"), ("cron", "Cron")],
        default="manual",
        required=True,
    )
    currency_rate_id = fields.Many2one("res.currency.rate", readonly=True, copy=False)
    name = fields.Char()

    _sql_constraints = [
        ("date_currency_company_uniq", "unique(date, currency_id, company_id)", "Ya existe tasa para esa fecha/moneda/compania."),
    ]

    def action_apply_to_odoo_rate(self):
        Rate = self.env["res.currency.rate"]
        for rec in self:
            existing = Rate.search([
                ("name", "=", rec.date),
                ("currency_id", "=", rec.currency_id.id),
                ("company_id", "=", rec.company_id.id),
            ], limit=1)
            vals = {
                "name": rec.date,
                "currency_id": rec.currency_id.id,
                "company_id": rec.company_id.id,
                "rate": rec.rate,
            }
            if existing:
                existing.write({"rate": rec.rate})
                rec.currency_rate_id = existing.id
            else:
                rec.currency_rate_id = Rate.create(vals).id
        return True

    @api.model
    def action_fetch_bcv_rate(self, source="manual"):
        raise UserError(_(
            "Configure la tasa manualmente o implemente el conector BCV. "
            "Cree un registro en Historico tasas BCV y pulse Aplicar a tasas Odoo."
        ))
