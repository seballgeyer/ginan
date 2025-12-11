import os
import sys

def _setdefault(k, v):
    if not os.environ.get(k):
        os.environ[k] = v

base = getattr(sys, "_MEIPASS", None)
if base:
    qt_base = os.path.join(base, "PySide6", "Qt")

    # Try multiple resource locations; stop at first that exists
    candidates = [
        os.path.join(qt_base, "resources"),
        os.path.join(qt_base, "lib", "QtWebEngineCore.framework", "Resources"),
    ]
    for res in candidates:
        if os.path.isdir(res):
            _setdefault("QTWEBENGINE_RESOURCES_PATH", res)
            loc = os.path.join(res, "qtwebengine_locales")
            _setdefault("QTWEBENGINE_LOCALES_PATH", loc)
            break

    # Helper path (macOS); harmless elsewhere
    exe_dir = os.path.dirname(sys.executable)
    helper = os.path.join(
        exe_dir,
        "Helpers",
        "QtWebEngineProcess.app",
        "Contents",
        "MacOS",
        "QtWebEngineProcess",
    )
    _setdefault("QTWEBENGINEPROCESS_PATH", helper)

    # Sandboxing and logging noise
    _setdefault("QTWEBENGINE_DISABLE_SANDBOX", "1")
    _setdefault(
        "QTWEBENGINE_CHROMIUM_FLAGS",
        "--no-sandbox --disable-gpu-sandbox --disable-seccomp-filter-sandbox --disable-logging --log-level=3",
    )
    _setdefault("QT_LOGGING_RULES", "qt.webengine.*=false")

    # Help QtWebEngineProcess resolve Qt frameworks on macOS
    if sys.platform == "darwin":
        libdir = os.path.join(qt_base, "lib")
        _setdefault("DYLD_FRAMEWORK_PATH", libdir)
        _setdefault("DYLD_LIBRARY_PATH", libdir)
