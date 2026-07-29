# Propuestas para maximizar la localización Venezuela (Odoo 19)

Roadmap técnico y de producto: de v1 sólida a solución **homologable, mantenible y competitiva**.

Prioridad: **P0** crítico · **P1** alto valor · **P2** diferenciación · **P3** largo plazo

---

## 1. Cumplimiento y homologación SENIAT (P0)

### Formatos oficiales
- Generadores byte-a-byte según instructivos del portal (longitud fija o separadores exactos).
- Plantillas de formato por año/resolución.
- Tests con golden files.

### XML ISLR / ARC
- XML conforme al esquema SENIAT; validación XSD si existe; numeración ARC.

### Auditoría y acceso SENIAT
- Rol solo lectura «consulta SENIAT».
- Log inmutable: emisión, anulación, exportación, cambios de secuencia.
- Hash/sello de documento (opcional).

### Secuencias
- Bloqueo de edición manual de number_next en producción.
- Secuencias por establecimiento/sucursal/serie autorizada.

### Paquete de evidencia
- Dataset demo + matriz «Providencia 121 ↔ pantalla/módulo».

---

## 2. Facturación fiscal avanzada (P0–P1)

- Desglose multi-alícuota real (16/8/31/exento) en factura y libros.
- NC/ND con documento afectado obligatorio (N° factura + control).
- PDF listo para imprenta; QR opcional.
- **Bridge a imprenta digital autorizada** (Providencia 102).
- POS con N° control y leyendas fiscales.

---

## 3. Retenciones (P0–P1)

**IVA:** wizard masivo del período; retenciones sufridas; TXT 100% layout oficial; dígito verificador RIF.

**ISLR:** tarifas por tramos/sustraendo UT; acumulados anuales por proveedor; conceptos versionados; PDF comprobante local.

**Municipales:** tasas por municipio y actividad económica.

---

## 4. IGTF y multi-moneda (P1)

- Política de traslado al cliente vs gasto empresa.
- Base imponible y exclusiones según norma.
- Reportes IGTF por período.
- Tasas BCV + dual currency en reportes (Bs + USD informativo).

---

## 5. Contabilidad (P1)

- Plan VEN-NIF mapeado sobre l10n_ve oficial.
- Cuentas predefinidas retenciones/IGTF/IVA.
- Cierre de ejercicio y ajuste por inflación si aplica.

---

## 6. Calidad de software (P0)

| Área | Acción |
|------|--------|
| Tests | Unitarios + integración flujos fiscales |
| CI | GitHub Actions Odoo 19 |
| Versionado | Tags semver = versión homologada |
| i18n | es_VE.po completo |
| Multi-company | company_id en impuestos y secuencias |
| Seguridad | ir.rule por compañía |

---

## 7. UX (P1)

- Wizard de configuración inicial (5 pasos).
- Dashboard «Cumplimiento del mes».
- Validación dígito RIF algoritmo SENIAT.
- Mensajes de error orientados a negocio.

---

## 8. Producto (P1–P2)

- Edición Homologada (tag + build certificado).
- Paquete Partner: manual + ficha técnica + evidencias.
- Roadmap público en GitHub Projects.
- Contribución OCA l10n-venezuela cuando estabilice.

---

## 9. Fases sugeridas

**Fase A (4–8 sem):** tests, multi-alícuota, TXT oficial, wizard config, dígito RIF, NC/ND enlazadas.

**Fase B (4–6 sem):** matriz 121, rol consulta, XML ISLR, paquete evidencia, política re-homologación.

**Fase C (6–12 sem):** imprenta digital, municipales, dashboard, POS, BCV.

**Fase D:** multi-sucursal, API integradores, App Store/OCA.

---

## 10. KPIs

% facturas con N° control automático · tiempo retenciones del mes · archivos rechazados por portal (→0) · onboarding cliente · cobertura tests · re-homologaciones sin incidentes.

---

## 11. Riesgos

| Riesgo | Mitigación |
|--------|------------|
| Cambio layout SENIAT | Formatos versionados por año |
| Homologación por versión | Branch homologado limpio |
| Multi-company | Tests + secuencias por company |
| % ISLR desactualizados | Data separada + aviso Gaceta |

---

## 12. Conclusión

La **v1** cubre el núcleo: RIF, IVA, retenciones, IGTF, N° control, libros, export.

Para **maximizar**: (1) formatos oficiales + tests P0, (2) multi-alícuota y NC/ND trazables, (3) auditoría y evidencia, (4) UX cierre de mes, (5) digital/POS/municipales como diferencial.

El Partner que versiona, documenta y re-homologa con disciplina tiene ventaja clara.
