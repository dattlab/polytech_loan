# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['polytech_loan.py'],
    pathex=[],
    binaries=[],
    datas=[
        ("ui/apply_rejected_dialog.ui", "."),
        ("ui/apply_success_dialog.ui", "."),
        ("ui/error_input.ui", "."),
        ("ui/exceed_max_amount_dialog.ui", "."),
        ("ui/invalid_cred_dialog.ui", "."),
        ("ui/invalid_email_dialog.ui", "."),
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='polytech_loan',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon="assets/app_logo.ico",
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
