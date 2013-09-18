#! /bin/sh
i18ndude rebuild-pot \
    --pot locales/plonehelpcenter.pot \
    --create plonehelpcenter \
    --merge locales/plonehelpcenter-manual.pot \
    .

for po in locales/*/LC_MESSAGES/plonehelpcenter.po; do
    i18ndude sync --pot locales/plonehelpcenter.pot $po
done
