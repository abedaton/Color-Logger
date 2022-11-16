
import logging
import logging.handlers
import sys
from functools import wraps
try:
    from colors import ColorCodes
except ModuleNotFoundError:
    from logger.colors import ColorCodes

class ConsoleFormatter(logging.Formatter):
    arg_colors: list[str] = [ColorCodes.pink, ColorCodes.light_blue]
    level_fields: list[str] = ["levelname", "levelno"]
    level_to_color: dict[int, str] = {
        logging.DEBUG: ColorCodes.green,
        logging.INFO: ColorCodes.blue,
        logging.WARNING: ColorCodes.orange,
        logging.ERROR: ColorCodes.red,
        logging.CRITICAL: ColorCodes.bold_red,
    }

    string_to_level: dict[str, int] = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }

    def __init__(self, fmt: str) -> None:
        super().__init__()
        self.level_to_formatter: dict[int, logging.Formatter] = {}

        def add_color_format(level: int) -> None:
            _format: str = self.level_to_color[level] + fmt + ColorCodes.reset
            formatter: logging.Formatter = logging.Formatter(_format)
            self.level_to_formatter[level] = formatter

        add_color_format(logging.DEBUG)
        add_color_format(logging.INFO)
        add_color_format(logging.WARNING)
        add_color_format(logging.ERROR)
        add_color_format(logging.CRITICAL)

    def rewrite_record(self, record: logging.LogRecord) -> None:
        msg: str = str(record.msg)
        msg: str = msg.replace("{", "_{{")
        msg: str = msg.replace("}", "_}}")
        placeholder_count: int = 0
        while True:
            if "_{{" not in msg:
                break
            color_index: int = placeholder_count % len(self.arg_colors)
            argcolor: str = self.arg_colors[color_index]
            msg: int = msg.replace("_{{", argcolor + "{", 1)
            msg: int = msg.replace("_}}", "}" + ColorCodes.reset + self.level_to_color[record.levelno], 1)
            placeholder_count += 1

        record.msg = msg.format(*record.args)
        record.args = []

    def format(self, record: logging.LogRecord) -> str:
        orig_msg: str = record.msg
        orig_args = record.args
        formatter: logging.Formatter = self.level_to_formatter.get(record.levelno)
        self.rewrite_record(record)
        formatted: str = formatter.format(record)
        record.msg = orig_msg
        record.args = orig_args
        return formatted

    def Watcher(level: str) -> callable:
        def _Watcher(func: callable) -> callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> callable:
                watcher: logging.Logger  = logging.getLogger("Logger")
                old_name: str = watcher.name
                watcher.name = "Watcher"
                if level == "DEBUG":
                    watcher.debug("Call: {0}({1}, {2})", func.__name__, args, kwargs)
                elif level == "INFO":
                    watcher.info("Call: {0}({1}, {2})", func.__name__, args, kwargs)
                elif level == "WARNING":
                    watcher.warning("Call: {0}({1}, {2})", func.__name__, args, kwargs)
                elif level == "ERROR":
                    watcher.error("Call: {0}({1}, {2})", func.__name__, args, kwargs)
                elif level == "CRITICAL":
                    watcher.critical("Call: {0}({1}, {2})", func.__name__, args, kwargs)
                watcher.name = old_name
                return func(*args, **kwargs)
            return wrapper
        return _Watcher



class FileFormatter(logging.Formatter):
    def __init__(self, fmt: str):
        super().__init__()
        self.formatter = logging.Formatter(fmt)
    
    def is_brace_format_style(self, record: logging.LogRecord) -> bool:
        if len(record.args) == 0:
            return False

        msg: str = record.msg
        if "%" in msg:
            return False
        
        count_of_start: int = msg.count("{")
        count_of_end: int = msg.count("}")

        if count_of_start != count_of_end:
            return False
        
        if count_of_start != len(record.args):
            return False

        return True

    def rewrite_record(self, record: logging.LogRecord) -> None:
        if not self.is_brace_format_style(record):
            return
        
        record.msg: str = record.msg.format(*record.args)
        record.args: list = []

    def format(self, record: logging.LogRecord) -> str:
        original_msg: str = record.msg
        original_args = record.args
        self.rewrite_record(record)
        formatted: str = self.formatter.format(record)

        record.msg: str = original_msg
        record.args = original_args
        return formatted

def init_logging(name, console_level, filename=None, console_format=None, file_format=None):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(stream=sys.stdout)
    console_handler.setLevel(console_level)
    if console_format is None:
        console_format = "%(asctime)s [%(levelname)-8s][%(name)s] - %(message)s (%(filename)s:%(lineno)d)"
    colored_formatter = ConsoleFormatter(console_format)
    console_handler.setFormatter(colored_formatter)
    root_logger.addHandler(console_handler)

    if filename is not None:
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel("DEBUG")
        if file_format is None:
            file_format = "%(asctime)s [%(name)s][%(levelname)-8s] - %(message)s - (%(filename)s:%(lineno)d)"
        file_handler.setFormatter(FileFormatter(file_format))
        root_logger.addHandler(file_handler)

    return logging.getLogger(name)






if __name__ == "__main__":
    logger = init_logging("Logger", "DEBUG", "log.log")

    @ConsoleFormatter.Watcher("INFO")
    def print_something(something1, something2):
        logger.info("{} {}", something1, something2)


    # logger.info("Hello World")
    # logger.info("Request from {} handled in {:.3f} ms", "127.0.0.1", 33.1)
    # logger.info("My favorite drinks are {}, {}, {}, {}", "milk", "wine", "tea", "beer")
    # logger.debug("this is a {} message", logging.getLevelName(logging.DEBUG))
    # logger.info("this is a {} message", logging.getLevelName(logging.INFO))
    logger.warning("this is a {} message", logging.getLevelName(logging.WARNING))
    # logger.error("this is a {} message", logging.getLevelName(logging.ERROR))
    # logger.critical("this is a {} message", logging.getLevelName(logging.CRITICAL))
    # logger.info("Does old-style formatting also work? %s it is, but no colors (yet)", True)



    print_something("hello", "world")
    logger.critical("this is a {} message", logging.getLevelName(logging.CRITICAL))