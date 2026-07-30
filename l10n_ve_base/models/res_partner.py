# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import re


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_ve_rif = fields.Char(string="RIF", tracking=True, copy=False)
    l10n_ve_taxpayer_type = fields.Selection(
        selection=[
            ("ordinary", "Contribuyente Ordinario"),
            ("special", "Contribuyente Especial"),
            ("formal", "Contribuyente Formal"),
            ("ordinary_no_agent", "Ordinario No Agente de Retencion"),
            ("exempt", "Exento / No sujeto"),
            ("public", "Ente Publico"),
            ("foreign", "Extranjero sin RIF"),
        ],
        string="Tipo de Contribuyente",
        default="ordinary",
        tracking=True,
    )
    l10n_ve_is_retention_agent = fields.Boolean(string="Es Agente de Retencion", default=False, tracking=True)
    l10n_ve_is_special_taxpayer = fields.Boolean(
        string="Es Contribuyente Especial",
        compute="_compute_l10n_ve_is_special_taxpayer",
        store=True,
    )
    l10n_ve_municipality_id = fields.Many2one(
        "res.country.state", string="Municipio / Estado",
        domain="[('country_id.code', '=', 'VE')]",
    )
    l10n_ve_parish = fields.Char(string="Parroquia")
    l10n_ve_economic_activity = fields.Char(string="Actividad Economica")

    @api.depends("l10n_ve_taxpayer_type")
    def _compute_l10n_ve_is_special_taxpayer(self):
        for partner in self:
            partner.l10n_ve_is_special_taxpayer = partner.l10n_ve_taxpayer_type == "special"

    @staticmethod
    def _l10n_ve_rif_check_digit(letter, number):
        letter_map = {"V": 1, "E": 2, "J": 3, "P": 4, "G": 5, "C": 6}
        weights = [3, 2, 7, 6, 5, 4, 3, 2]
        body = (number or "").zfill(8)[-8:]
        total = letter_map.get(letter.upper(), 0) * 4
        for i, ch in enumerate(body):
            total += int(ch) * weights[i]
        remainder = total % 11
        check = 0 if remainder < 2 else 11 - remainder
        return str(check)

    @api.model
    def l10n_ve_validate_rif(self, rif):
        if not rif:
            return True, "", ""
        rif_clean = rif.strip().upper().replace(" ", "").replace(".", "")
        m = re.match(r"^([VJEGPC])[-]?([0-9]{6,9})[-]?([0-9])$", rif_clean)
        if not m:
            return False, _("Formato invalido. Ej: J-12345678-9"), rif_clean
        letter, number, digit = m.groups()
        expected = self._l10n_ve_rif_check_digit(letter, number)
        normalized = "%s-%s-%s" % (letter, number, digit)
        if digit != expected:
            return False, _("Digito verificador incorrecto. Se esperaba %s.") % expected, normalized
        return True, "", normalized

    @api.constrains("l10n_ve_rif")
    def _check_l10n_ve_rif(self):
        for partner in self:
            if not partner.l10n_ve_rif:
                continue
            ok, msg, _n = partner.l10n_ve_validate_rif(partner.l10n_ve_rif)
            if not ok:
                raise ValidationError(_("RIF invalido (%s): %s") % (partner.l10n_ve_rif, msg))

    @api.onchange("l10n_ve_rif")
    def _onchange_l10n_ve_rif(self):
        if not self.l10n_ve_rif:
            return
        ok, msg, normalized = self.l10n_ve_validate_rif(self.l10n_ve_rif)
        if normalized:
            self.l10n_ve_rif = normalized
        if not ok:
            return {"warning": {"title": _("RIF"), "message": msg}}

    @api.onchange("vat", "country_id")
    def _onchange_vat_country_ve(self):
        if self.country_id and self.country_id.code == "VE" and self.vat and not self.l10n_ve_rif:
            self.l10n_ve_rif = self.vat

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("l10n_ve_rif"):
                vals["l10n_ve_rif"] = vals["l10n_ve_rif"].strip().upper()
            if vals.get("country_id"):
                country = self.env["res.country"].browse(vals["country_id"])
                if country.code == "VE" and vals.get("l10n_ve_rif") and not vals.get("vat"):
                    vals["vat"] = vals["l10n_ve_rif"]
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("l10n_ve_rif"):
            vals["l10n_ve_rif"] = vals["l10n_ve_rif"].strip().upper()
        return super().write(vals)
