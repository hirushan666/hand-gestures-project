# GestureMouse.spec - Advanced PyInstaller configuration
# Save this file in your HGP root directory

import sys
import os
from PyInstaller.utils.hooks import collect_data_files, collect_submodules, collect_dynamic_libs
from glob import glob

block_cipher = None

# Get all Python files from core directory
core_files = []
for py_file in glob('core/*.py'):
    core_files.append((py_file, 'core'))

# Collect all necessary data files
datas = [
    ('assets', 'assets'),
] + core_files

# Collect hidden imports for mediapipe, cv2, and mouse control libraries
hiddenimports = [
    'PIL',
    'PIL._tkinter_finder',
    'cv2',
    'numpy',
    'mediapipe',
    'pyautogui',
    'pynput',
    'autopy',
    'mouse',
    'subprocess',
    'tkinter',
    'tkinter.ttk',
] + collect_submodules('mediapipe') + collect_submodules('cv2')

# Add mediapipe data files
datas += collect_data_files('mediapipe')

# Collect autopy binaries (needed for mouse control)
try:
    datas += collect_data_files('autopy')
except:
    pass

a = Analysis(
    ['frontend/launcher.py', 'frontend/mode_runners.py'],
    pathex=['core', 'frontend'],  # Add core and frontend to the path
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['runtime_hook.py'],  # Add runtime hook to fix sys.path
    excludes=['scipy', 'pandas', 'torch', 'tensorflow'],  # Exclude unused large libraries (keep matplotlib for mediapipe)
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
    name='GestureMouseController',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,  # Compress with UPX (reduce file size)
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',  # Add your icon file
)