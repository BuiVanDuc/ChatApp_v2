import os.path
import threading
from datetime import datetime

from my_log.function import singleton
from settings import LOG_SETTINGS
from my_log.color_console import sync_color_console


class Logger:
    _instance = None

    def __init__(self):
        """
        Init function
        logs_folder: Logfile directory
        log_file: log filename
        log_level: Log level
        :return:
        """
        self.logs_folder = LOG_SETTINGS.get("log_dir")
        if not os.path.exists(self.logs_folder):
            os.makedirs(os.path.realpath(self.logs_folder))
        if not os.path.exists(self.logs_folder):
            sync_color_console.error("Cannot create logs folder: " + str(self.logs_folder))
            exit()
        log_prefix = LOG_SETTINGS.get("log_prefix")
        self.error_log_file = os.path.join(self.logs_folder, log_prefix + "_error_logs.txt")
        self.info_log_file = os.path.join(self.logs_folder, log_prefix + "_info_logs.txt")
        self.log_level = LOG_SETTINGS.get("log_level").lower()
        self.log_mode = LOG_SETTINGS.get("log_mode").lower()

    @staticmethod
    def is_backup(log_file):
        try:
            return os.path.getsize(log_file) > LOG_SETTINGS.get("max_log_file_size")
        except Exception:
            pass
        return False

    def error(self, call_module, data):
        """
        Write error log functions
        :param call_module: module or file name
        :param data: log string
        :return: log string is write and print if log_level is error or all
        """
        try:
            if self.log_level != "all" and self.log_level != "error":
                return False
            data_log = "[+] {}\t{}\t{}\n".format(datetime.now().strftime(LOG_SETTINGS.get("log_date_format")), call_module, str(data))
            if self.log_mode == "file" or self.log_mode == "all":
                threading.Lock()
                if Logger.is_backup(self.error_log_file):
                    backup_file_name = os.path.join(self.logs_folder, "{}_error_{}.txt".format(LOG_SETTINGS.get("log_prefix"), datetime.now().strftime('%H_%M_%S %d-%m-%Y')))
                    os.rename(self.error_log_file, backup_file_name)
                _writer = open(self.error_log_file, "a+")
                _writer.write(data_log)
                _writer.close()
                threading.RLock()
            if self.log_mode == "console" or self.log_mode == "all":
                sync_color_console.error(data_log)
        except Exception as ex:
            sync_color_console.error("Cannot write error log: " + str(ex))

    def info(self, call_module, data):
        """
        Write error log functions
        :param call_module: module or file name
        :param data: log string
        :return: log string is write and print if log_level is error or all
        """
        try:
            if self.log_level != "all" and self.log_level != "info":
                return False
            data_log = "[+] {}\t{}\t{}\n".format(datetime.now().strftime(LOG_SETTINGS.get("log_date_format")), call_module, str(data))
            if self.log_mode == "file" or self.log_mode == "all":
                threading.Lock()
                if Logger.is_backup(self.info_log_file):
                    backup_file_name = os.path.join(self.logs_folder, "{}_info_{}.txt".format(LOG_SETTINGS.get("log_prefix"), datetime.now().strftime('%H_%M_%S %d-%m-%Y')))
                    os.rename(self.info_log_file, backup_file_name)
                _writer = open(self.info_log_file, "a+")
                _writer.write(data_log)
                _writer.close()
                threading.RLock()
            if self.log_mode == "console" or self.log_mode == "all":
                sync_color_console.info(data_log)
        except Exception as ex:
            sync_color_console.error("Cannot write error log: " + str(ex))

    def console(self, data):
        data_log = "[+] {}\t{}\n".format(datetime.now().strftime(LOG_SETTINGS.get("log_date_format")), str(data))
        sync_color_console.info(data_log)


sync_logger = singleton(Logger)
