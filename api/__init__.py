import os

DEBUG = bool(os.environ.get("CASPIAN_DEBUG", "false").strip().lower() == "true")
