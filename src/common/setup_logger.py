import logging


def setup_logger(log_filename, log_level=logging.ERROR):
    """
    setup_logger 函数用于设置并返回一个 logger 对象

    参数:
    log_filename: 日志文件的名称
    log_level: 日志级别，默认为 logging.ERROR
    """
    # 创建一个 logger 对象
    logger = logging.getLogger(log_filename)
    # 设置日志级别
    logger.setLevel(log_level)
    # 创建一个文件处理器，并将日志级别设置为 log_level
    handler = logging.FileHandler(log_filename)
    handler.setLevel(log_level)
    # 将处理器添加到 logger
    logger.addHandler(handler)
    # 返回 logger 对象
    return logger


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


if __name__ == '__main__':
    logger = get_logger(name='test', log_file_path='../logs/test.log')
    logger.error('图一乐')