{
    "name": "Venezuela - Retencion de IVA",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Retencion IVA 75%/100% y wizard masivo",
    "author": "Partner Oficial Odoo Venezuela",
    "license": "LGPL-3",
    "depends": ["l10n_ve_withholding"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/mass_withholding_wizard_views.xml",
        "views/account_move_views.xml",
        "views/account_withholding_views.xml",
    ],
    "installable": True,
    "application": False,
}
