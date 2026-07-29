# Matriz Providencia SNAT/2024/000121 ↔ Localización Odoo

| Requisito Providencia 121 | Implementación en `l10n_ve_seniat` | Módulo | Evidencia |
|---------------------------|-------------------------------------|--------|-----------|
| Integridad de registros | Estados de retención; no eliminar confirmados/declarados | withholding | Comprobante Confirmado/Declarado |
| Continuidad / correlativo | Secuencias `no_gap` N° control | invoice | Publicar factura → control correlativo |
| Trazabilidad | Chatter + timestamps emisión/confirmación/anulación | invoice, withholding | Campos datetime |
| Inalterabilidad | Bloqueo borrador/unlink con control emitido | invoice | button_draft en emitida |
| Correcciones solo NC/ND | Bloqueo edición; documento origen en NC | invoice | `l10n_ve_origin_move_id` |
| Remisión electrónica | Export TXT (base); API/imprenta = fase 2 | reports | Wizard export |
| Clave consulta SENIAT | Rol lectura (fase B); ir.rule company | withholding | multi-company |
| Retenciones IVA | 75%/100% + comprobante + asiento | withholding_iva | Factura compra |
| Retenciones ISLR | Conceptos + UT + comprobante | withholding_islr | Flujo ISLR |
| Timestamps | emission_datetime, confirmed_date | invoice, withholding | Formulario |
| Versionado | Tags Git + manifest 19.0.x | todos | GitHub releases |

## Demo mínima para evaluación técnica

1. Configurar compañía (asistente SENIAT) + secuencias.
2. Publicar 3 facturas de venta → N° control 1,2,3 sin huecos.
3. Emitir NC vinculada a factura 1 (`l10n_ve_origin_move_id`).
4. Intentar eliminar factura publicada → error.
5. Retención IVA 75% y 100% sobre compras.
6. Retención ISLR con concepto.
7. Libro de ventas + PDF.
8. Export TXT del mes.

## Notas

- Remisión continua API SENIAT no está en v1; usar TXT/XML portal o bridge imprenta digital (Fase C).
- Cada versión mayor debe re-homologarse.
