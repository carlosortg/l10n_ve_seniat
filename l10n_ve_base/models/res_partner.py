# -*- coding: utf-8 -*-
import re
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    l10n_ve_rif = fields.Char(
        string="RIF",
        help="Registro de Informacion Fiscal. Formato: J-12345678-9",
        index=True,
    )
    l10n_ve_contributor_type = fields.Selection(
        selection=[
            ("ordinary", "Contribuyente ordinario"),
            ("special", "Contribuyente especial"),
            ("formal", "Contribuyente formal"),
            ("exempt", "Exento"),
            ("other", "Otro"),
        ],
        string="Tipo de contribuyente",
        default="ordinary",
    )
    l10n_ve_person_type = fields.Selection(
        selection=[
            ("natural", "Persona natural"),
            ("juridica", "Persona juridica"),
        ],
        string="Tipo de persona",
        compute="_compute_l10n_ve_person_type",
        store=True,
        readonly=False,
    )

    @api.depends("l10n_ve_rif", "company_type")
    def _compute_l10n_ve_person_type(self):
        for partner in self:
            rif = (partner.l10n_ve_rif or partner.vat or "").upper().strip()
            letter = rif[0] if rif else ""
            if letter in ("V", "E", "P"):
                partner.l10n_ve_person_type = "natural"
            elif letter in ("J", "G", "C"):
                partner.l10n_ve_person_type = "juridica"
            elif partner.company_type == "company":
                partner.l10n_ve_person_type = "juridica"
            else:
                partner.l10n_ve_person_type = "natural"

    @api.constrains("l10n_ve_rif")
    def _check_l10n_ve_rif(self):
        for partner in self:
            if partner.l10n_ve_rif:
                partner._l10n_ve_validate_rif(partner.l10n_ve_rif)

    @api.model
    def _l10n_ve_validate_rif(self, rif):
        """Valida formato y digito verificador (modulo 11)."""
        if not rif:
            return True
        cleaned = re.sub(r"[\s.-]", "", rif.upper())
        m = re.match(r"^([VEJPGC])(\d{7,8})(\d)$", cleaned)
        if not m:
            raise ValidationError(
                _("RIF invalido: %s. Use formato J-12345678-9") % rif
            )
        letter, body, check = m.group(1), m.group(2), int(m.group(3))
        letter_map = {"V": 4, "E": 8, "J": 12, "P": 16, "G": 20, "C": 24}
        weights = [3, 2, 7, 6, 5, 4, 3, 2]
        body = body.zfill(8)
        total = letter_map[letter]
        for i, digit in enumerate(body):
            total += int(digit) * weights[i]
        remainder = total % 11
        expected = 0 if remainder in (0, 1) else 11 - remainder
        if expected != check:
            raise ValidationError(
                _("Digito verificador de RIF incorrecto: %s (esperado %s)")
                % (rif, expected)
            )
        return True

    @api.onchange("l10n_ve_rif")
    def _onchange_l10n_ve_rif(self):
        if self.l10n_ve_rif and not self.vat:
            self.vat = self.l10n_ve_rif
