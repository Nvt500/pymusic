# -*- mode: python ; coding: utf-8 -*-

import sys
from PyInstaller.utils.hooks import copy_metadata

datas = []
datas += copy_metadata('imageio')
datas += copy_metadata('moviepy')

a = Analysis(
    ['pymusic.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
    strip=(not sys.platform.startswith('win')),
    upx=True,
    upx_exclude=[],
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='pymusic',
    debug=False,
    bootloader_ignore_signals=False,
    strip=(not sys.platform.startswith('win')),
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)