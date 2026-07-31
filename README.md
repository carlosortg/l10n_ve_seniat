# Localizacion Venezuela SENIAT (Odoo 19)

Modulos `l10n_ve_*` para facturacion fiscal, retenciones, libros, bancos y tasa BCV.

## Instalacion en Coolify

1. Deploy con `docker-compose.yml` (`build: .`).
2. Logs deben listar modulos bajo `/mnt/extra-addons/l10n_ve_seniat`.
3. Actualizar lista de aplicaciones e instalar en orden:

```
l10n_ve_base
l10n_ve_account
l10n_ve_withholding
l10n_ve_withholding_iva
l10n_ve_withholding_islr
l10n_ve_invoice
l10n_ve_igtf
l10n_ve_fiscal_book
l10n_ve_reports
l10n_ve_bank
l10n_ve_currency_bcv
```

## Enterprise

Ver `DEPLOY_ENTERPRISE.md` (repo privado odoo/enterprise branch 19.0).

## Repo

https://github.com/carlosortg/l10n_ve_seniat
