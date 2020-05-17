"""Simplify logging creation no needed parameter """
import os
import datetime
import logging
from pprint import pformat


class Logger:
    """
    Customized logger class having get_logger method returning a logger

    params: [all are optional]
        name = filename to pass generally it is __name__
        level = specify level for Hfilehandler (info is default)
        file = file to write log messages to (project.log is default)
        mode = which mode to write. Default['a']
        debug_file = specify debug mode file
        debug_mode = specify which mode to use default['w']
        console [bool] = swictch console logging on or off.
    """

    def __init__(
        self,
        name=None,
        level="info",
        mode="a",
        debug_mode="w",
        file_name=None,
        debug_file=None,
        console=True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.name = name
        self.level = self.level_parser(level)
        self.file = file_name if file_name else self.get_file_name()
        self.mode = mode
        self.debug_mode = debug_mode
        self.console = console
        self.debug_file = debug_file

    @staticmethod
    def level_parser(key):
        """
        logging attrs mapping to strs for easy parameter setting.
        param = 'debug', 'warning' etc in str
        output = logging.DEBUG, logging.Warning etc attributes
        """
        level_dict = {
            "debug": logging.DEBUG,
            "warning": logging.WARNING,
            "error": logging.ERROR,
            "info": logging.INFO,
            "fatal": logging.FATAL,
            "critical": logging.CRITICAL,
        }
        return level_dict[key]

    @staticmethod
    def handle_file(file):
        """
        Checks if file exists else creates directory upto that file.
        Params:
            file : Input file
        """
        if not os.path.exists(file):
            try:
                if os.path.split(file)[0] != "":
                    os.makedirs(os.path.split(file)[0])

                with open(file, "w") as wf:
                    pass
            except FileExistsError:
                pass

    def get_logger(self):
        """
        returns a logger as specified in Logger class
        """
        if self.name is None:
            import inspect

            caller = inspect.currentframe().f_back
            self.name = caller.f_globals["__name__"]

        logger = logging.getLogger(self.name)
        logger.setLevel(logging.DEBUG)

        # create formatter
        format_style = (
            "\n\n"
            "%(asctime)s : %(name)s : %(funcName)s :"
            "%(lineno)s : %(levelname)s:"
            "\n"
            "%(message)s"
        )
        formatter = logging.Formatter(format_style)

        if self.console:
            # create console handler and set level to debug
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            # add formatter to console_handler
            console_handler.setFormatter(formatter)
            # add console_handler to logger
            logger.addHandler(console_handler)

        # create file handler and set level
        self.handle_file(self.file)
        filehandler = logging.FileHandler(self.file, mode=self.mode)
        filehandler.setLevel(self.level)
        filehandler.setFormatter(formatter)
        logger.addHandler(filehandler)

        if self.debug_file:
            self.handle_file(self.debug_file)
            debug_filehandler = logging.FileHandler(
                self.debug_file, mode=self.debug_mode
            )
            debug_filehandler.setLevel(logging.DEBUG)
            debug_filehandler.setFormatter(formatter)
            logger.addHandler(debug_filehandler)
        return logger

    @staticmethod
    def get_file_name():
        utc_time = datetime.datetime.utcnow()
        offset = datetime.timedelta(minutes=5 * 60 + 45)
        nepal_time = utc_time + offset
        file_name = nepal_time.strftime("%b_%d_%Y_%-I:%M_%p") + ".log"
        return file_name


def prettify(data):
    if isinstance(data, str):
        formatted_data = pformat(data)
    else:
        formatted_data = pformat(data, indent=2)
    return f"\n{formatted_data}"
