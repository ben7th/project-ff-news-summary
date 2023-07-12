import logging
import sys

class RedColorFormatter(logging.Formatter):
    red_start = "\033[31m"
    color_end = "\033[0m"

    def format(self, record):
        message = super().format(record)
        if record.levelno >= logging.ERROR:
            message = self.red_start + message + self.color_end
        return message

def get_logger(name, log_file_path, log_level=logging.DEBUG, console_level=logging.ERROR):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 创建一个输出到文件的 handler，并设置级别为 DEBUG
    file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
    file_handler.setLevel(log_level)

    # 创建一个输出到控制台的 handler，并设置级别为 ERROR
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)

    # 创建一个 formatter，指定日志记录的格式
    msg_str = '[%(levelname)s] [%(name)s] [%(asctime)s] %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter(msg_str, datefmt=datefmt)
    red_color_formatter = RedColorFormatter(msg_str, datefmt=datefmt)

    # 将 formatter 添加到两个 handler
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(red_color_formatter)

    # 将两个 handler 添加到 logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


import loguru
# 禁用日志输出到命令行
loguru.logger.remove()

def get_loguru_logger(name: str, log_file_path: str, log_level: str = 'DEBUG', console_level: str = 'ERROR'):
    new_logger = loguru.logger.bind(name=name)

    # 添加文件处理器
    new_logger.add(log_file_path, rotation="500 MB", level=log_level,
        filter=lambda record: record["extra"].get("name") == name)

    # 添加控制台处理器
    new_logger.add(sys.stderr, level=console_level, 
        filter=lambda record: record["extra"].get("name") == name)
    
    return new_logger