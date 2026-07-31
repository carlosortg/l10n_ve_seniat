# -*- coding: utf-8 -*-
from odoo import fields, models, _


class L10nVeComplianceDashboard(models.TransientModel):
    _name = "l10n.ve.compliance.dashboard"
    _description = "Dashboard cumplimiento fiscal VE"

    company_id = fields.Many2one("res.company", required=True, default=lambda self: self.env.company)
    date_from = fields.Date(required=True, default=lambda self: fields.Date.today().replace(day=1))
    date_to = fields.Date(required=True, default=fields.Date.today)
    sale_invoices = fields.Integer(readonly=True)
    sale_without_control = fields.Integer(readonly=True)
    iva_withholdings_draft = fields.Integer(readonly=True)
    notes = fields.Html(readonly=True)

    def action_refresh(self):
        self.ensure_one()
        Move = self.env["account.move"]
        Wh = self.env["account.withholding"]
        sales = Move.search([
            ("company_id", "=", self.company_id.id),
            ("move_type", "in", ("out_invoice", "out_refund")),
            ("state", "=", "posted"),
            ("invoice_date", ">=", self.date_from),
            ("invoice_date", "<=", self.date_to),
        ])
        without = sales.filtered(lambda m: not getattr(m, "l10n_ve_control_number", None))
        draft = Wh.search_count([
            ("company_id", "=", self.company_id.id),
            ("withholding_type", "=", "iva"),
            ("state", "=", "draft"),
            ("date", ">=", self.date_from),
            ("date", "<=", self.date_to),
        ])
        self.write({
            "sale_invoices": len(sales),
            "sale_without_control": len(without),
            "iva_withholdings_draft": draft,
            "notes": "<ul><li>Ventas: %s</li><li>Sin N control: %s</li><li>Ret IVA borrador: %s</li></ul>" % (
                len(sales), len(without), draft),
        })
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }
