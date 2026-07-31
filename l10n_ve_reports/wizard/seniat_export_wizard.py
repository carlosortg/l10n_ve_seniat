# -*- coding: utf-8 -*-
import base64
from odoo import fields, models, _
from odoo.exceptions import UserError


class L10nVeSeniatExportWizard(models.TransientModel):
    _name = "l10n.ve.seniat.export.wizard"
    _description = "Exportar retenciones SENIAT"

    date_from = fields.Date(required=True, default=lambda self: fields.Date.today().replace(day=1))
    date_to = fields.Date(required=True, default=fields.Date.today)
    company_id = fields.Many2one("res.company", default=lambda self: self.env.company, required=True)
    export_type = fields.Selection([("iva_txt", "TXT IVA"), ("islr_txt", "TXT ISLR")], default="iva_txt", required=True)
    file_data = fields.Binary(readonly=True)
    file_name = fields.Char(readonly=True)
    state = fields.Selection([("draft", "Draft"), ("done", "Done")], default="draft")

    def action_export(self):
        self.ensure_one()
        wtype = "iva" if self.export_type == "iva_txt" else "islr"
        whs = self.env["account.withholding"].search([
            ("company_id", "=", self.company_id.id),
            ("withholding_type", "=", wtype),
            ("state", "in", ("confirmed", "declared")),
            ("date", ">=", self.date_from),
            ("date", "<=", self.date_to),
        ])
        if not whs:
            raise UserError(_("No hay retenciones en el periodo."))
        lines = ["fecha;numero;rif;base;retenido"]
        for w in whs:
            rif = (w.partner_id.l10n_ve_rif or w.partner_id.vat or "").replace("-", "")
            lines.append(";".join([
                w.date.strftime("%Y-%m-%d") if w.date else "",
                w.name or "",
                rif,
                "%.2f" % w.amount_base,
                "%.2f" % w.amount_withheld,
            ]))
        content = "\n".join(lines) + "\n"
        self.write({
            "file_data": base64.b64encode(content.encode("utf-8")),
            "file_name": "retenciones_%s.txt" % wtype,
            "state": "done",
        })
        return {
            "type": "ir.actions.act_window",
            "res_model": self._name,
            "res_id": self.id,
            "view_mode": "form",
            "target": "new",
        }
