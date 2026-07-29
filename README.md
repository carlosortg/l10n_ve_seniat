# Localización Venezolana para Odoo 19 — SENIAT

Localización fiscal orientada a **cumplimiento y homologación SENIAT** (Providencia SNAT/2024/000121).

**Versión actual: 19.0.1.1.0**

## Módulos

| Módulo | Descripción |
|--------|-------------|
| `l10n_ve_base` | RIF (dígito verificador), contribuyente, wizard config SENIAT |
| `l10n_ve_account` | IVA 16/8/31/0%, posiciones fiscales |
| `l10n_ve_withholding` | Motor de retenciones + inalterabilidad |
| `l10n_ve_withholding_iva` | Retención IVA 75%/100% |
| `l10n_ve_withholding_islr` | Conceptos ISLR + UT |
| `l10n_ve_igtf` | IGTF en pagos en divisas |
| `l10n_ve_invoice` | N° control, secuencias, NC/ND con documento origen, PDF |
| `l10n_ve_fiscal_book` | Libros compras/ventas multi-alícuota + PDF |
| `l10n_ve_reports` | Export TXT declaraciones |

## Documentación

- [MANUAL_DE_USO.md](MANUAL_DE_USO.md) — operación completa
- [MEJORAS_PROPUESTAS.md](MEJORAS_PROPUESTAS.md) — roadmap P0–P3
- [MATRIZ_PROVIDENCIA_121.md](MATRIZ_PROVIDENCIA_121.md) — requisitos ↔ implementación
- [CHANGELOG.md](CHANGELOG.md)

## Instalación

```text
l10n_ve_base → l10n_ve_account → l10n_ve_withholding →
l10n_ve_withholding_iva → l10n_ve_withholding_islr →
l10n_ve_igtf → l10n_ve_invoice → l10n_ve_fiscal_book → l10n_ve_reports
```

Luego: **Contabilidad → Configuración → Configuración inicial SENIAT**

## Licencia

LGPL-3
