FROM odoo:19.0
USER root
RUN mkdir -p /mnt/extra-addons/l10n_ve_seniat
COPY l10n_ve_base /mnt/extra-addons/l10n_ve_seniat/l10n_ve_base
COPY l10n_ve_account /mnt/extra-addons/l10n_ve_seniat/l10n_ve_account
COPY l10n_ve_withholding /mnt/extra-addons/l10n_ve_seniat/l10n_ve_withholding
COPY l10n_ve_withholding_iva /mnt/extra-addons/l10n_ve_seniat/l10n_ve_withholding_iva
COPY l10n_ve_withholding_islr /mnt/extra-addons/l10n_ve_seniat/l10n_ve_withholding_islr
COPY l10n_ve_igtf /mnt/extra-addons/l10n_ve_seniat/l10n_ve_igtf
COPY l10n_ve_invoice /mnt/extra-addons/l10n_ve_seniat/l10n_ve_invoice
COPY l10n_ve_fiscal_book /mnt/extra-addons/l10n_ve_seniat/l10n_ve_fiscal_book
COPY l10n_ve_reports /mnt/extra-addons/l10n_ve_seniat/l10n_ve_reports
COPY l10n_ve_bank /mnt/extra-addons/l10n_ve_seniat/l10n_ve_bank
COPY l10n_ve_currency_bcv /mnt/extra-addons/l10n_ve_seniat/l10n_ve_currency_bcv
RUN chown -R odoo:odoo /mnt/extra-addons
USER odoo
