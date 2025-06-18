# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=['.'],  # Add your project root path
    binaries=[],
    datas=[
        ('static/*', 'static'),
        ('.env', '.'),
        ('src/*.py', 'src'),
    ],
    hiddenimports=[
        'fastapi',
        'uvicorn',
        'uvicorn.loops.auto',
        'uvicorn.protocols.http.auto',
        'uvicorn.protocols.websockets.auto',
        'pydantic',
        'email_validator',
        'python-dotenv',
        'anyio',
        'httptools',
        'click',
        'h11',
        'typing_extensions',
        'src.routes',
        'src.app',
        'src.supabase_client',
        'src.services',
        'src.schemas',
        # Add any other imports your routes use
    ],
    hookspath=['.'],  # Add path to your hooks if any
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
    name='resignee_tracker_2',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
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