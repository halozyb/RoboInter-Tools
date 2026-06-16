# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for RoboInter-Tools
Single EXE: server + client, auto-detect MP4 files, ready to use.
"""
import os
from PyInstaller.utils.hooks import collect_data_files

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config/config.yaml', 'config'),
        ('asserts', 'asserts'),
        ('user_config', 'user_config'),
        ('client/client.py', 'client'),
        ('client/utils.py', 'client'),
        ('server/server.py', 'server'),
        ('README.md', '.'),
    ] + collect_data_files('PyQt5'),
    hiddenimports=[
        'PyQt5',
        'PyQt5.QtCore',
        'PyQt5.QtGui',
        'PyQt5.QtWidgets',
        'numpy',
        'numpy.core._methods',
        'numpy.lib.format',
        'cv2',
        'yaml',
        'flask',
        'flask.app',
        'flask.helpers',
        'flask.json',
        'werkzeug',
        'werkzeug.serving',
        'portalocker',
        'requests',
        'imageio',
        'imageio_ffmpeg',
        'PIL',
        'matplotlib',
        'matplotlib.backends.backend_qt5agg',
        'server',
        'server.server',
        'client',
        'client.client',
        'client.utils',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'torch',
        'sam2',
    ],
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
    name='RoboInter-Tools',
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
    icon='aaa.png' if os.path.exists('aaa.png') else None,
)
