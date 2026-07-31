{
    "name": "Venezuela - Tasa BCV",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Historico tasas BCV y aplicacion a monedas Odoo",
    "author": "Partner Oficial Odoo Venezuela",
    "license": "LGPL-3",
    "depends": ["account", "l10n_ve_base"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "views/bcv_rate_views.xml",
        "views/res_config_settings_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
    "application": False,
}
