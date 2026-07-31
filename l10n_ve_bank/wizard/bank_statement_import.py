# -*- coding: utf-8 -*-
import base64, csv, io
from datetime import datetime
from odoo import fields, models, _
from odoo.exceptions import UserError


class L10nVeBankStatementImport(models.TransientModel):
    _name = "l10n.ve.bank.statement.import"
    _description = "Importar extracto CSV VE"

    journal_id = fields.Many2one("account.journal", required=True, domain="[('type', '=', 'bank')]")
    data_file = fields.Binary(required=True)
    filename = fields.Char()
    delimiter = fields.Selection([("semicolon", ";"), ("comma", ",")], default="semicolon", required=True)
    has_header = fields.Boolean(default=True)

    def action_import(self):
        self.ensure_one()
        raw = base64.b64decode(self.data_file)
        text = raw.decode("utf-8-sig", errors="replace")
        sep = ";" if self.delimiter == "semicolon" else ","
        rows = list(csv.reader(io.StringIO(text), delimiter=sep))
        if self.has_header and rows:
            rows = rows[1:]
        StatementLine = self.env["account.bank.statement.line"]
        created = StatementLine
        for row in rows:
            if len(row) < 4:
                continue
            try:
                date = datetime.strptime(row[0].strip(), "%d/%m/%Y").date()
                amount = float(row[3].replace(",", ".").replace(" ", ""))
            except Exception:
                continue
            created |= StatementLine.create({
                "date": date,
                "payment_ref": (row[1] or "/")[:64],
                "narration": row[2] if len(row) > 2 else row[1],
                "amount": amount,
                "journal_id": self.journal_id.id,
            })
        if not created:
            raise UserError(_("No se importaron movimientos."))
        return {
            "type": "ir.actions.act_window",
            "res_model": "account.bank.statement.line",
            "domain": [("id", "in", created.ids)],
            "view_mode": "list,form",
        }
