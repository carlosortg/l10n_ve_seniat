# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class L10nVeMassWithholdingWizard(models.TransientModel):
    _name = "l10n.ve.mass.withholding.wizard"
    _description = "Generar retenciones IVA masivas"

    date_from = fields.Date(required=True, default=lambda self: fields.Date.today().replace(day=1))
    date_to = fields.Date(required=True, default=fields.Date.today)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)
    rate = fields.Selection([("75", "75%"), ("100", "100%")], default="75", required=True)

    def action_generate(self):
        self.ensure_one()
        moves = self.env["account.move"].search([
            ("company_id", "=", self.company_id.id),
            ("move_type", "in", ("in_invoice", "in_refund")),
            ("state", "=", "posted"),
            ("invoice_date", ">=", self.date_from),
            ("invoice_date", "<=", self.date_to),
        ])
        if not moves:
            raise UserError(_("No hay facturas de compra en el periodo."))
        Wh = self.env["account.withholding"]
        created = self.env["account.withholding"]
        pct = float(self.rate)
        for move in moves:
            iva = sum(move.line_ids.filtered(lambda l: l.tax_line_id).mapped("balance"))
            iva = abs(iva)
            if iva <= 0:
                continue
            created |= Wh.create({
                "partner_id": move.partner_id.id,
                "withholding_type": "iva",
                "date": move.invoice_date or fields.Date.context_today(self),
                "amount_base": iva,
                "rate": pct,
                "amount_withheld": iva * pct / 100.0,
                "l10n_ve_iva_retention_rate": self.rate,
                "invoice_ids": [(4, move.id)],
                "company_id": self.company_id.id,
            })
        return {
            "type": "ir.actions.act_window",
            "name": _("Retenciones generadas"),
            "res_model": "account.withholding",
            "view_mode": "list,form",
            "domain": [("id", "in", created.ids)],
        }
