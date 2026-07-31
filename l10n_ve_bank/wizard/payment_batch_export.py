# -*- coding: utf-8 -*-
import base64
from odoo import fields, models, _
from odoo.exceptions import UserError


class L10nVePaymentBatchExport(models.TransientModel):
    _name = "l10n.ve.payment.batch.export"
    _description = "Exportar pagos masivos VE"

    date_from = fields.Date()
    date_to = fields.Date()
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)
    file_data = fields.Binary(readonly=True)
    file_name = fields.Char(readonly=True)
    state = fields.Selection([("draft", "Draft"), ("done", "Done")], default="draft")

    def action_generate(self):
        self.ensure_one()
        domain = [
            ("company_id", "=", self.company_id.id),
            ("payment_type", "=", "outbound"),
            ("state", "in", ("in_process", "paid", "posted")),
        ]
        if self.date_from:
            domain.append(("date", ">=", self.date_from))
        if self.date_to:
            domain.append(("date", "<=", self.date_to))
        payments = self.env["account.payment"].search(domain)
        if not payments:
            raise UserError(_("No hay pagos."))
        lines = ["cuenta;monto;rif;nombre;ref"]
        for p in payments:
            acc = "".join(c for c in (p.partner_bank_id.acc_number or "") if c.isdigit())
            rif = (p.partner_id.l10n_ve_rif or p.partner_id.vat or "").replace("-", "")
            lines.append(";".join([acc, "%.2f" % p.amount, rif, (p.partner_id.name or "")[:40], p.name or ""]))
        content = "\n".join(lines) + "\n"
        self.write({
            "file_data": base64.b64encode(content.encode("utf-8")),
            "file_name": "pagos_ve.csv",
            "state": "done",
        })
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }
