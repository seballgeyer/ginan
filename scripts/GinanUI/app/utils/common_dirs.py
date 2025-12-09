import sys
from pathlib import Path

def get_base_path():
    """Get the base path for resources, handling both development and PyInstaller bundled modes."""
    if getattr(sys, 'frozen', False):
        # Running in PyInstaller bundle
        return Path(sys._MEIPASS)
    else:
        # Running in development mode
        return Path(__file__).parent.parent

BASE_PATH = get_base_path()
TEMPLATE_PATH = BASE_PATH / "resources" / "Yaml" / "default_config.yaml"
GENERATED_YAML = BASE_PATH / "resources" / "ppp_generated.yaml"
INPUT_PRODUCTS_PATH = BASE_PATH / "resources" / "inputData" / "products"
