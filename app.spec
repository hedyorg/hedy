# -*- mode: python ; coding: utf-8 -*-
from os import path
import sys

dirname = 'offlinehedy'
appname = 'run-hedy-server'

# Find the venv directory. We need to be able to pass this to
# pyinstaller, otherwise it will not bundle the libraries we installed
# from the venv.
venv_dir = [p for p in sys.path if 'site-packages' in p][0]


data_files = [
    # Files
    ('README.md', '.'),
    ('static_babel_content.json', '.'),

    # Folders
    ('content', 'content'),
    ('coursedata', 'coursedata'),
    ('grammars', 'grammars'),
    ('grammars-Total', 'grammars-Total'),
    ('prefixes', 'prefixes'),
    ('static', 'static'),
    ('templates', 'templates'),
    ('translations', 'translations'),
]

a = Analysis(
    ['app.py'],
    pathex=[venv_dir],
    binaries=[],
    datas=data_files,
    hiddenimports=[],
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=dirname,
)
