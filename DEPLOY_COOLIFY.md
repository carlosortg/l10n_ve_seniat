# Despliegue Odoo 19 + Localización VE en Coolify (VPS)

Windows (dev) → GitHub → VPS + Coolify → Odoo 19

## Pasos rápidos

1. Push del repo a GitHub (incluir Dockerfile y docker-compose.coolify.yml).
2. Coolify → New → Docker Compose → repo `carlosortg/l10n_ve_seniat`.
3. Compose file: `docker-compose.coolify.yml`.
4. Variable: `POSTGRES_PASSWORD` (fuerte).
5. Deploy + dominio HTTPS.
6. Crear BD (país Venezuela) e instalar módulos `l10n_ve_*` en orden.
7. Configuración inicial SENIAT.

## Orden de módulos

```
l10n_ve_base → account → withholding → withholding_iva → withholding_islr
→ igtf → invoice → fiscal_book → reports → bank → currency_bcv
```

## Local Windows (Docker Desktop)

```powershell
docker compose up -d --build
# http://localhost:8069
```

## Tasa BCV

Menú Contabilidad → Traer tasa BCV ahora / Histórico tasas BCV.
Ajustes → actualizar automáticamente (cron diario).

Documentación completa en el archivo DEPLOY_COOLIFY.md del proyecto.
