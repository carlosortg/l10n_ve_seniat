# Localización Venezolana para Odoo 19 — SENIAT

Localización fiscal completa orientada al cumplimiento y a la **homologación ante el SENIAT** (Providencia Administrativa SNAT/2024/000121).

## Módulos

| Módulo | Descripción | Estado |
|--------|-------------|--------|
| `l10n_ve_base` | RIF, tipo contribuyente, estados VE, campos fiscales | ✅ |
| `l10n_ve_account` | IVA 16/8/31/0%, posiciones fiscales, cuentas retenciones | ✅ |
| `l10n_ve_withholding` | Motor genérico de retenciones + secuencias + inalterabilidad | ✅ |
| `l10n_ve_withholding_iva` | Retención IVA 75%/100%, comprobantes, asiento | ✅ |
| `l10n_ve_withholding_islr` | Conceptos ISLR, UT, retención, comprobantes | ✅ |
| `l10n_ve_igtf` | IGTF sobre pagos en divisas | ✅ |
| `l10n_ve_invoice` | N° control, secuencias SENIAT, PDF factura fiscal | ✅ |
| `l10n_ve_fiscal_book` | Libro de compras y ventas + PDF | ✅ |
| `l10n_ve_reports` | Exportación TXT declaraciones IVA / ISLR | ✅ |

## Requisitos

- **Odoo 19.0**
- Módulos: `account`, `purchase` (para flujos de compra)
- País de la compañía: Venezuela

## Instalación

```text
# Añadir al addons_path y actualizar apps
# Orden sugerido:
l10n_ve_base → l10n_ve_account → l10n_ve_withholding →
l10n_ve_withholding_iva → l10n_ve_withholding_islr →
l10n_ve_igtf → l10n_ve_invoice → l10n_ve_fiscal_book → l10n_ve_reports
```

Ver **[MANUAL_DE_USO.md](MANUAL_DE_USO.md)** para configuración y operación completa.
Ver **[MEJORAS_PROPUESTAS.md](MEJORAS_PROPUESTAS.md)** para el roadmap de maximización.

## Homologación SENIAT (Providencia 121)

La localización contempla:

- Integridad y trazabilidad de registros
- Número de control correlativo (`no_gap`)
- Correcciones solo mediante NC/ND
- Timestamps de emisión / confirmación
- Retenciones de IVA e ISLR
- Exportación de archivos para declaración

La homologación la solicita el **partner domiciliado en Venezuela** sobre una **versión concreta** del software.

## Licencia

LGPL-3

## Autor

Partner Oficial Odoo Venezuela
