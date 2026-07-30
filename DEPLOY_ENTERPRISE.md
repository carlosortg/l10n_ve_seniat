# Odoo Enterprise 19 + localizacion VE en Coolify

Requisito: acceso a https://github.com/odoo/enterprise (Partner).

## Arquitectura

- Imagen `odoo:19.0` (Community)
- `/mnt/enterprise` = clone branch `19.0` del repo enterprise
- `/mnt/extra-addons/l10n_ve_seniat` = este repo (Dockerfile COPY)

addons-path: community, /mnt/enterprise, /mnt/extra-addons/l10n_ve_seniat

## Montar Enterprise en el VPS

```bash
export GH_TOKEN=ghp_xxx   # PAT con acceso a odoo/enterprise
mkdir -p /data/odoo-enterprise
git clone --depth 1 --branch 19.0 \
  https://${GH_TOKEN}@github.com/odoo/enterprise.git \
  /data/odoo-enterprise
```

En Coolify: Persistent Storage del servicio odoo, destino `/mnt/enterprise`, origen `/data/odoo-enterprise`.

No subas enterprise a un repo publico.
