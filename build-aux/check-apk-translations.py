#!/usr/bin/env python3
"""Fail a release build if Android APKs omit or cannot read Chinese catalogs."""
import gettext
import io
import sys
import zipfile


def check_apk(path):
    with zipfile.ZipFile(path) as apk:
        prefix = 'assets/share/locale/zh_CN/LC_MESSAGES/'
        for domain in ('live-photo-conv', 'gtk40', 'libadwaita'):
            name = prefix + domain + '.mo'
            if name not in apk.namelist():
                raise ValueError(f'{path}: missing Chinese catalog {name}')
            catalog = gettext.GNUTranslations(io.BytesIO(apk.read(name)))
            if domain == 'live-photo-conv':
                for source in ('Make Live Photo', 'Live Photo Converter', 'OK'):
                    if catalog.gettext(source) == source:
                        raise ValueError(f'{path}: untranslated {source!r}')
                if '%u' not in catalog.ngettext('%u file selected', '%u files selected', 2):
                    raise ValueError(f'{path}: file count placeholder is missing')
        print(f'{path}: Chinese application and toolkit catalogs verified')


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: check-apk-translations.py APK [APK ...]')
    for path in sys.argv[1:]:
        check_apk(path)
