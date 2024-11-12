# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('sf_app/gui/img/sf_icon.png', 'sf_app/gui/img'),
        ('sf_app/gui/img/sf_icon.ico', 'sf_app/gui/img'),
        ('sf_app/gui/img/sf_logo.png', 'sf_app/gui/img'),
        ('sf_app/gui/fonts/Roboto-Regular.ttf', 'sf_app/gui/fonts'),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='sf_archiver',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['sf_app/gui/img/sf_icon.ico'],
)
