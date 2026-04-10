#----------------------------------------------------------
# PyInstaller configuration file
#
# This file controls how we build a standalone distribution of
# Hedy that can run in environments where Internet access might
# be spotty.
#----------------------------------------------------------
# -*- mode: python ; coding: utf-8 -*-
from os import path
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

dirname = 'offlinehedy'
appname = 'run-hedy-server'

# Find the venv directory. We need to be able to pass this to
# pyinstaller, otherwise it will not bundle the libraries we installed
# from the venv.
venv_dir = [p for p in sys.path if 'site-packages' in p][0]

# hedy loads some files (for example in hedy/prefixes/*.py) directly from disk
# at import time, so they must be added as data files explicitly.
hedy_hiddenimports = collect_submodules('hedy')
hedy_data_files = collect_data_files('hedy')
hedy_prefix_py_files = collect_data_files('hedy.prefixes', include_py_files=True)

data_files = [
    # Files
    ('README.md', '.'),
    ('static_babel_content.json', '.'),

    # Folders
    ('content', 'content'),
    ('static', 'static'),
    ('templates', 'templates'),
    ('translations', 'translations'),
]

data_files += hedy_data_files + hedy_prefix_py_files

a = Analysis(
    ['app.py'],
    pathex=[venv_dir],
    binaries=[],
    datas=data_files,
    hiddenimports=hedy_hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=appname,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon="static/images/Hedy-logo.ico",
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name=dirname,
)
