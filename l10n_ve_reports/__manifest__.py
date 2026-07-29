{
    "name": "Venezuela - Reportes y Declaraciones SENIAT",
    "version": "19.0.1.4.0",
    "category": "Accounting/Localizations",
    "summary": "TXT/XML SENIAT, dashboard de cumplimiento fiscal",
    "author": "Partner Oficial Odoo Venezuela",
    "license": "LGPL-3",
    "depends": [
        "l10n_ve_withholding",
        "l10n_ve_withholding_iva",
        "l10n_ve_withholding_islr",
    ],
    "data": [
        "security/ir.model.access.csv",
        "wizard/seniat_export_wizard_views.xml",
        "views/compliance_dashboard_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
    "application": False,
}
