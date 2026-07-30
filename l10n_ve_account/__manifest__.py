{
    "name": "Venezuela - Contabilidad",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "IVA y posiciones fiscales Venezuela",
    "author": "Partner Oficial Odoo Venezuela",
    "license": "LGPL-3",
    "depends": ["account", "l10n_ve_base"],
    "data": [
        "data/account_tax_data.xml",
        "data/account_fiscal_position_data.xml",
        "views/account_tax_views.xml",
        "views/res_company_views.xml",
    ],
    "installable": True,
    "application": False,
}
