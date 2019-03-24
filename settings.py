import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOG_SETTINGS = {
    "log_folder": os.getenv("LOG_FOLDER", "logs"),
    "log_dir": os.path.join(BASE_DIR, "my_log", os.getenv("LOG_FOLDER", "logs")),
    "log_prefix": os.getenv("LOG_PREFIX", "chat_"),
    "log_level": os.getenv("LOG_LEVEL", "all"),
    "log_mode": os.getenv("LOG_MODE", "all"),
    "log_date_format": os.getenv("LOG_DATE_FORMAT", "%H:%M:%S %d-%m-%Y"),
    "max_log_file_size": int(os.getenv("MAX_LOG_FILE_SIZE", "10485760"))
}