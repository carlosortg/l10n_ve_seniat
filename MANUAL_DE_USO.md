# Manual de Uso Completo — Localización Venezuela Odoo 19 (SENIAT)

| Campo | Valor |
|-------|--------|
| **Producto** | `l10n_ve_seniat` |
| **Versión** | 19.0.1.0.0 |
| **Odoo** | 19.0 |
| **Licencia** | LGPL-3 |
| **Normativa principal** | Providencia SNAT/2024/000121 (Gaceta Oficial N° 43.032) |
| **Objetivo** | Cumplimiento fiscal y soporte a homologación ante el SENIAT |

---

## Índice

1. Introducción y alcance
2. Arquitectura de módulos
3. Requisitos previos
4. Instalación paso a paso
5. Configuración inicial (checklist maestro)
6. Datos maestros: partners y compañía
7. Impuestos y posiciones fiscales
8. Secuencias SENIAT y número de control
9. Facturación de ventas
10. Retención de IVA
11. Retención de ISLR
12. IGTF
13. Libros fiscales
14. Exportación de declaraciones (TXT)
15. Reportes PDF
16. Reglas de inalterabilidad y homologación
17. Menús y navegación
18. Flujos de trabajo recomendados
19. Errores frecuentes y soluciones
20. Checklist pre-homologación SENIAT
21. Limitaciones de la v1
22. Glosario
23. Anexos

---

## 1. Introducción y alcance

Esta localización adapta **Odoo 19** a las obligaciones fiscales venezolanas: RIF, IVA (16/8/31/0%), retenciones IVA (75%/100%) e ISLR (conceptos + UT), IGTF, número de control correlativo, libros de compras/ventas, exportación TXT y controles de inalterabilidad (Providencia 121).

**No sustituye** asesoría tributaria. Homologación: el SENIAT autoriza al **proveedor domiciliado en Venezuela** y a **versiones concretas**.

---

## 2. Arquitectura de módulos

`l10n_ve_base` → account → withholding → (iva | islr | reports) ; igtf ; invoice → fiscal_book

Orden instalación: base, account, withholding, withholding_iva, withholding_islr, igtf, invoice, fiscal_book, reports.

---

## 3. Requisitos previos

Odoo 19, account (+ purchase), país VE, preferible moneda VES, entorno de pruebas.

---

## 4. Instalación

1. Copiar al addons_path  2. Reiniciar  3. Actualizar apps  4. Instalar en el orden de la sección 2.

---

## 5. Checklist de configuración

**Compañía:** RIF, tipo contribuyente, agente retención, **Crear secuencias SENIAT**, cuentas IVA/ISLR/IGTF, % IGTF.

**Diarios ventas:** secuencia N° control (no_gap).

**Partners:** RIF, tipo contribuyente (75/100), tipo persona ISLR.

**UT y conceptos ISLR:** valores vigentes Gaceta.

**Prueba:** factura con control, PDF fiscal, retención IVA, libro ventas.

---

## 6. Partners y compañía

RIF formato J-12345678-9. Especial/sin RIF/extranjero → retención IVA **100%**. Ordinario con RIF → **75%**. Tipo persona natural/jurídica define % ISLR.

---

## 7. Impuestos

IVA 16%, 8%, 31%, Exento, Exportación, Retención IVA 75%/100%. Posiciones: Ordinario, Especial, Exento, Exportación, Público, Extranjero.

---

## 8. Secuencias y N° de Control

Correlativo sin huecos. Asignación al **publicar** ventas. Configurar en Compañía (botón) o Diario (pestaña SENIAT). También F/, NC/, ND/.

---

## 9. Facturación ventas

Publicar → N° Control automático → PDF Factura Fiscal VE. Correcciones **solo NC/ND**.

---

## 10. Retención IVA

Desde factura de compra publicada: Crear Retención IVA. Estados: Borrador → Confirmado → Declarado. No anular si Declarado. Asiento si hay cuenta configurada.

---

## 11. Retención ISLR

Conceptos + Unidad Tributaria. Crear Retención ISLR; % según persona y concepto; base imponible; mínimo UT opcional.

---

## 12. IGTF

Pagos inbound en moneda ≠ VES; % configurable (default 3%); cuenta IGTF; validar exclusiones con asesor.

---

## 13. Libros fiscales

Informes → Libros Fiscales: Ventas/Compras, período, Generar, PDF. Resumen por alícuota. NC restan.

---

## 14. Export TXT SENIAT

Retenciones VE → Exportar declaración: IVA o ISLR, período, descargar. Validar layout oficial del portal antes de subir.

---

## 15. PDF

Factura Fiscal VE (RIF, control, autorización, totales). Libro Fiscal VE desde asistente.

---

## 16. Inalterabilidad

No editar N° control; no eliminar factura publicada con control; no anular retención Declarada; correcciones solo NC/ND; timestamps de emisión/confirmación.

---

## 17. Menús

Contabilidad → Retenciones VE (comprobantes, IVA, ISLR, conceptos, UT, export) · Informes → Libros · Configuración diarios SENIAT.

---

## 18. Cierre de mes

Facturas compra → retenciones → confirmar → libros → export TXT → portal SENIAT → marcar Declarado.

---

## 19. Errores frecuentes

Sin secuencia → crear en compañía. 100% inesperado → completar RIF. Sin botón → publicar factura. Libro vacío → solo posted. TXT vacío → confirmar retenciones.

---

## 20. Checklist pre-homologación

Ficha técnica, manual usuario/técnico, domicilio VE, demo N° control + NC/ND + retenciones + timestamps + libros + export, tag Git de versión, solo vender versiones homologadas.

---

## 21. Limitaciones v1

TXT base tabular; XML ISLR formal pendiente; multi-alícuota simplificada; sin API SENIAT ni imprenta digital; municipales parciales.

---

## 22. Glosario

SENIAT · RIF · IVA · ISLR · UT · IGTF · N° Control · NC/ND · Agente de retención · Homologación · Providencia 121

---

## 23. Anexos

Instalación: base→account→withholding→iva→islr→igtf→invoice→fiscal_book→reports. Licencia LGPL-3. Mantener UT, % ISLR y layouts del portal.

---

*Manual v19.0.1.0.0 — Localización Venezuela SENIAT Odoo 19.*
