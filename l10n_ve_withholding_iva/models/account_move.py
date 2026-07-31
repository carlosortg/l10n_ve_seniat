# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = "account.move"

    l10n_ve_iva_withholding_rate = fields.Selection(
        selection=[("75", "75%"), ("100", "100%")],
        string="% retencion IVA",
        help="Usado al generar la retencion desde la factura de compra.",
    )

    def action_l10n_ve_create_iva_withholding(self):
        """Genera comprobante de retencion IVA a partir de facturas de compra publicadas."""
        Wh = self.env["account.withholding"]
        created = Wh
        for move in self:
            if move.state != "posted":
                raise UserError(_("Solo facturas publicadas: %s") % move.name)
            if move.move_type not in ("in_invoice", "in_refund"):
                raise UserError(_("Solo facturas de compra / NC proveedor."))
            iva = move._l10n_ve_get_tax_amount()
            if iva <= 0:
                raise UserError(_("La factura %s no tiene IVA retenible.") % move.name)
            # Determinar tasa: campo, o 100% si contribuyente especial, else 75%
            partner = move.partner_id.commercial_partner_id
            if move.l10n_ve_iva_withholding_rate:
                rate_sel = move.l10n_ve_iva_withholding_rate
            elif partner.l10n_ve_taxpayer_type == "special" or partner.l10n_ve_is_special_taxpayer:
                rate_sel = "100"
            else:
                rate_sel = "75"
            pct = float(rate_sel)
            amount_wh = iva * pct / 100.0
            if move.move_type == "in_refund":
                amount_wh = -amount_wh
                iva = -iva
            wh = Wh.create({
                "partner_id": partner.id,
                "withholding_type": "iva",
                "date": move.invoice_date or fields.Date.context_today(self),
                "company_id": move.company_id.id,
                "amount_base": abs(iva),
                "rate": pct,
                "amount_withheld": abs(amount_wh),
                "l10n_ve_iva_retention_rate": rate_sel,
                "invoice_ids": [(4, move.id)],
                "line_ids": [(0, 0, {
                    "invoice_id": move.id,
                    "amount_base": abs(iva),
                    "rate": pct,
                    "amount_withheld": abs(amount_wh),
                })],
                "notes": _("Generado desde factura %s") % move.name,
            })
            created |= wh
        if len(created) == 1:
            return {
                "type": "ir.actions.act_window",
                "res_model": "account.withholding",
                "res_id": created.id,
                "view_mode": "form",
            }
        return {
            "type": "ir.actions.act_window",
            "name": _("Retenciones IVA"),
            "res_model": "account.withholding",
            "view_mode": "list,form",
            "domain": [("id", "in", created.ids)],
        }
