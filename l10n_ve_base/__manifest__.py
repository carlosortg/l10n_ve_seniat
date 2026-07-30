{
    "name": "Venezuela - Base",
    "version": "19.0.1.1.0",
    "category": "Accounting/Localizations",
    "summary": "RIF, tipo contribuyente y base fiscal Venezuela / SENIAT",
    "author": "Partner Oficial Odoo Venezuela",
    "license": "LGPL-3",
    "depends": ["base", "account"],
    "data": [
        "security/ir.model.access.csv",
        "data/res.country.state.csv",
        "views/res_partner_views.xml",
        "views/res_company_views.xml",
        "wizard/seniat_config_wizard_views.xml",
    ],
    "installable": True,
    "application": False,
}
