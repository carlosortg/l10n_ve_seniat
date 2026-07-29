# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class L10nVeFiscalBookWizard(models.TransientModel):
    _name = "l10n.ve.fiscal.book.wizard"
    _description = "Asistente Libro Fiscal Venezuela"

    book_type = fields.Selection(
        selection=[
            ("sale", "Libro de Ventas"),
            ("purchase", "Libro de Compras"),
        ],
        string="Tipo de Libro",
        required=True,
        default="sale",
    )
    date_from = fields.Date(required=True, default=lambda self: fields.Date.today().replace(day=1))
    date_to = fields.Date(required=True, default=fields.Date.today)
    company_id = fields.Many2one(
        "res.company", required=True, default=lambda self: self.env.company
    )

    def action_generate(self):
        self.ensure_one()
        Move = self.env["account.move"]
        if self.book_type == "sale":
            types = ("out_invoice", "out_refund")
        else:
            types = ("in_invoice", "in_refund")
        moves = Move.search([
            ("company_id", "=", self.company_id.id),
            ("move_type", "in", types),
            ("state", "=", "posted"),
            ("invoice_date", ">=", self.date_from),
            ("invoice_date", "<=", self.date_to),
        ], order="invoice_date, name")
        if not moves:
            raise UserError(_("No hay facturas en el período seleccionado."))
        return {
            "type": "ir.actions.act_window",
            "name": _("Facturas del libro"),
            "res_model": "account.move",
            "view_mode": "list,form",
            "domain": [("id", "in", moves.ids)],
            "target": "current",
        }
