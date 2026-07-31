{
    "name": "Venezuela - Reportes SENIAT",
    "version": "19.0.1.4.0",
    "category": "Accounting/Localizations",
    "summary": "Dashboard cumplimiento y exportacion retenciones",
    "author": "Partner Oficial Odoo Venezuela",
    "license": "LGPL-3",
    "depends": ["l10n_ve_withholding", "l10n_ve_withholding_iva", "l10n_ve_withholding_islr"],
    "data": [
        "security/ir.model.access.csv",
        "views/compliance_dashboard_views.xml",
        "wizard/seniat_export_wizard_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
    "application": False,
}
