#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import controller
import locale
import gettext
from pathlib import Path

if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    LOCALE_DIR = Path(__file__).parent / "locale"
    # Nombre de la base de datos
    locale.bindtextdomain('InterfazMusical', LOCALE_DIR)
    gettext.bindtextdomain('InterfazMusical', LOCALE_DIR)
    gettext.textdomain('InterfazMusical')

    runner = controller.Controller()
    runner.start()
