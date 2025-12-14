# -*- mode: python ; coding: utf-8 -*-

import os
import sys
import glob
from PyInstaller.utils.hooks import (
    collect_submodules,
    collect_data_files,
)

# Resolve repo root from the current working directory (workflow invokes from repo root)
REPO_ROOT = os.path.abspath(os.getcwd())
APP_DIR = os.path.join(REPO_ROOT, "scripts", "GinanUI")
PYI_HOOK = os.path.join(APP_DIR, "pyinstaller", "qtwebengine_runtime_hook.py")

# Primary script
main_script = os.path.join(APP_DIR, "main.py")

# Datas (source, dest within bundle)
datas = []
# App package assets
datas += [(os.path.join(APP_DIR, "app"), "app")]
# Plot script used at runtime
plot_src = os.path.join(REPO_ROOT, "scripts", "plot_pos.py")
if os.path.exists(plot_src):
    datas += [(plot_src, "scripts")]

# Binaries (executables and shared libs) bundled under 'bin'
binaries = []
bin_dir = os.path.join(REPO_ROOT, "bin")
if os.path.isdir(bin_dir):
    for path in glob.glob(os.path.join(bin_dir, "*")):
        binaries.append((path, "bin"))

# Hidden imports and package collections
hiddenimports = []

# Core app modules
hiddenimports += [
    "scripts.GinanUI.app",
    "scripts.GinanUI.app.models",
    "scripts.GinanUI.app.models.execution",
    "scripts.GinanUI.app.controllers",
    "scripts.GinanUI.app.controllers.input_controller",
    "scripts.GinanUI.app.controllers.visualisation_controller",
    "scripts.GinanUI.app.utils",
    "scripts.GinanUI.app.utils.workers",
    "scripts.GinanUI.app.utils.cddis_credentials",
    "scripts.GinanUI.app.utils.cddis_email",
    "scripts.GinanUI.app.utils.common_dirs",
    "scripts.GinanUI.app.utils.gn_functions",
    "scripts.GinanUI.app.utils.yaml",
    "scripts.GinanUI.app.views.main_window_ui",
]

# Scientific stack
for pkg in ("numpy", "pandas", "scipy", "statsmodels"):
    hiddenimports += collect_submodules(pkg)
    datas += collect_data_files(pkg)

# Qt WebEngine
hiddenimports += collect_submodules("PySide6")
hiddenimports += collect_submodules("PySide6.QtWebEngineCore")
hiddenimports += collect_submodules("PySide6.QtWebEngineWidgets")
datas += collect_data_files("PySide6.QtWebEngineCore")
datas += collect_data_files("PySide6.QtWebEngineWidgets")

# Try to include QtWebEngineProcess.app on macOS
try:
    import PySide6
    qt_dir = os.path.join(os.path.dirname(PySide6.__file__), "Qt")
    helper1 = os.path.join(qt_dir, "libexec", "QtWebEngineProcess.app")
    helper2 = os.path.join(qt_dir, "lib", "QtWebEngineCore.framework", "Helpers", "QtWebEngineProcess.app")
    if sys.platform == "darwin":
        if os.path.exists(helper1):
            binaries.append((helper1, "Helpers"))
        elif os.path.exists(helper2):
            binaries.append((helper2, "Helpers"))
except Exception:
    pass

# Build
block_cipher = None

a = Analysis(
    [main_script],
    pathex=[REPO_ROOT],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[PYI_HOOK],
    excludes=[],
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
    name='GinanUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='GinanUI'
)
