{
    "name": "Venezuela - Base",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Campos y validaciones base para la localización venezolana (RIF, tipo contribuyente, dirección fiscal)",
    "author": "Partner Oficial Odoo Venezuela",
    "license": "LGPL-3",
    "depends": ["base", "account"],
    "data": [
        "data/res.country.state.csv",
        "views/res_partner_views.xml",
        "views/res_company_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
