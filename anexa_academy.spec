# -*- mode: python ; coding: utf-8 -*-
a = Analysis(
    ['client/src/main.py'],
    pathex=['.'],
    binaries=[],
    datas=[('client/src/styles', 'client/src/styles')],
    hiddenimports=['PySide6', 'httpx', 'fpdf2', 'plyer'],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data)
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AnexaAcademy',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
)
