{
    "name": "Venezuela - Retención de IVA",
    "version": "19.0.1.4.0",
    "category": "Accounting/Localizations",
    "summary": "Retención IVA 75%/100%, comprobantes, wizard masivo",
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
