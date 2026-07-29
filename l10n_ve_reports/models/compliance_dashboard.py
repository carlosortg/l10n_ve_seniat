# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class L10nVeComplianceDashboard(models.TransientModel):
    _name = "l10n.ve.compliance.dashboard"
    _description = "Dashboard cumplimiento fiscal VE"

    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company,
    )
    date_from = fields.Date(required=True, default=lambda self: fields.Date.today().replace(day=1))
    date_to = fields.Date(required=True, default=fields.Date.today)

    sale_invoices = fields.Integer(readonly=True)
    sale_without_control = fields.Integer(string="Ventas sin N° control", readonly=True)
    purchase_invoices = fields.Integer(readonly=True)
    iva_withholdings_draft = fields.Integer(readonly=True)
    iva_withholdings_confirmed = fields.Integer(readonly=True)
    iva_withholdings_declared = fields.Integer(readonly=True)
    islr_withholdings_draft = fields.Integer(readonly=True)
    islr_withholdings_confirmed = fields.Integer(readonly=True)
    islr_withholdings_declared = fields.Integer(readonly=True)
    amount_iva_withheld = fields.Float(readonly=True)
    amount_islr_withheld = fields.Float(readonly=True)
    partners_without_rif = fields.Integer(readonly=True)
    notes = fields.Html(string="Alertas", readonly=True)

    def action_refresh(self):
        self.ensure_one()
        company = self.company_id
        Move = self.env["account.move"]
        Wh = self.env["account.withholding"]

        sales = Move.search([
            ("company_id", "=", company.id),
            ("move_type", "in", ("out_invoice", "out_refund")),
            ("state", "=", "posted"),
            ("invoice_date", ">=", self.date_from),
            ("invoice_date", "<=", self.date_to),
        ])
        without_control = sales.filtered(lambda m: not getattr(m, "l10n_ve_control_number", None))
        purchases = Move.search([
            ("company_id", "=", company.id),
            ("move_type", "in", ("in_invoice", "in_refund")),
            ("state", "=", "posted"),
            ("invoice_date", ">=", self.date_from),
            ("invoice_date", "<=", self.date_to),
        ])

        def _wh_count(wtype, state):
            return Wh.search_count([
                ("company_id", "=", company.id),
                ("withholding_type", "=", wtype),
                ("state", "=", state),
                ("date", ">=", self.date_from),
                ("date", "<=", self.date_to),
            ])

        def _wh_amount(wtype):
            whs = Wh.search([
                ("company_id", "=", company.id),
                ("withholding_type", "=", wtype),
                ("state", "in", ("confirmed", "declared")),
                ("date", ">=", self.date_from),
                ("date", "<=", self.date_to),
            ])
            return sum(whs.mapped("amount_withheld"))

        partners_no_rif = self.env["res.partner"].search_count([
            ("parent_id", "=", False),
            ("country_id.code", "=", "VE"),
            ("l10n_ve_rif", "=", False),
            ("vat", "=", False),
            ("active", "=", True),
            ("customer_rank", ">", 0),
        ])

        alerts = []
        if without_control:
            alerts.append("<li><b>%s</b> facturas de venta sin N° de control.</li>" % len(without_control))
        if _wh_count("iva", "draft"):
            alerts.append("<li>Retenciones de <b>IVA en borrador</b>.</li>")
        if _wh_count("islr", "draft"):
            alerts.append("<li>Retenciones de <b>ISLR en borrador</b>.</li>")
        if partners_no_rif:
            alerts.append("<li><b>%s</b> clientes VE sin RIF.</li>" % partners_no_rif)
        if not alerts:
            alerts.append("<li>Sin alertas críticas en el período.</li>")

        self.write({
            "sale_invoices": len(sales),
            "sale_without_control": len(without_control),
            "purchase_invoices": len(purchases),
            "iva_withholdings_draft": _wh_count("iva", "draft"),
            "iva_withholdings_confirmed": _wh_count("iva", "confirmed"),
            "iva_withholdings_declared": _wh_count("iva", "declared"),
            "islr_withholdings_draft": _wh_count("islr", "draft"),
            "islr_withholdings_confirmed": _wh_count("islr", "confirmed"),
            "islr_withholdings_declared": _wh_count("islr", "declared"),
            "amount_iva_withheld": _wh_amount("iva"),
            "amount_islr_withheld": _wh_amount("islr"),
            "partners_without_rif": partners_no_rif,
            "notes": "<ul>%s</ul>" % "".join(alerts),
        })
        return {
            "type": "ir.actions.act_window",
            "res_model": "l10n.ve.compliance.dashboard",
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }
