FROM odoo:19.0

USER root

COPY . /tmp/l10n_src/

RUN mkdir -p /mnt/extra-addons/l10n_ve_seniat /mnt/enterprise \
    && for d in /tmp/l10n_src/l10n_ve_*; do \
         if [ -d "$d" ] && [ -f "$d/__manifest__.py" ]; then \
           cp -a "$d" /mnt/extra-addons/l10n_ve_seniat/; \
         fi; \
       done \
    && chown -R odoo:odoo /mnt/extra-addons /mnt/enterprise \
    && rm -rf /tmp/l10n_src \
    && echo "=== Modulos VE en imagen ===" \
    && ls -1 /mnt/extra-addons/l10n_ve_seniat/

USER odoo
