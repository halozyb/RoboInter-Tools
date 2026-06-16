# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec for RoboInter-Tools Client
Packages the PyQt5 annotation client as a standalone Windows exe.
"""
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

block_cipher = None

# Collect PyQt5 data files
pyqt5_datas = collect_data_files('PyQt5')

a = Analysis(
    ['client/client.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config/config.yaml', 'config'),
        ('asserts', 'asserts'),
        ('user_config', 'user_config'),
        ('README.md', '.'),
    ] + pyqt5_datas,
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
        'portalocker',
        'requests',
        'imageio',
        'imageio_ffmpeg',
        'PIL',
        'matplotlib',
        'matplotlib.backends.backend_qt5agg',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'torch',
        'sam2',
        'sam',
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
    console=True,  # Show console for server output
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='aaa.png' if os.path.exists('aaa.png') else None,
)
