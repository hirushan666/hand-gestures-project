"""
Runtime hook for PyInstaller to fix module import paths.
This ensures core modules can find HandTrackingModule when running as EXE.
"""
import sys
import os

# Add the core directory to sys.path at runtime
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    bundle_dir = sys._MEIPASS
    core_path = os.path.join(bundle_dir, 'core')
    if core_path not in sys.path:
        sys.path.insert(0, core_path)
