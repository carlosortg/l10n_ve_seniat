{
    "name": "Venezuela - Libros Fiscales SENIAT",
    "version": "19.0.1.0.0",
    "category": "Accounting/Localizations",
    "summary": "Libro de compras y ventas",
    "author": "Partner Oficial Odoo Venezuela",
    "license": "LGPL-3",
    "depends": ["account", "l10n_ve_base", "l10n_ve_invoice"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/fiscal_book_wizard_views.xml",
        "views/menu_views.xml",
    ],
    "installable": True,
    "application": False,
}
