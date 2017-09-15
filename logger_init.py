from logging import *
import logging.handlers
from painter import *
import os
import time

MNT_PATH = ''
LOG_PATH = MNT_PATH + 'logs'

logging_level = logging.DEBUG  # choose: DEBUG, INFO, WARNING


class ColoredLogging(Logger):
    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)

    def debug(self, msg, *args, **kwargs):
        if self.isEnabledFor(DEBUG):
            self._log(DEBUG, paint(msg, MAGENTA), args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        if self.isEnabledFor(WARNING):
            self._log(WARNING, paint(msg, YELLOW), args, **kwargs)

    def error(self, msg, *args, **kwargs):
        if self.isEnabledFor(ERROR):
            self._log(ERROR, paint(msg, RED), args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        if self.isEnabledFor(CRITICAL):
            self._log(CRITICAL, paint(msg, RED_INV), args, **kwargs)


class ColoredLogger:
    def __init__(self):
        print('\n\n '+paint('[sys][logger]', GREEN)+' INITIALIZING\n')
        if not os.path.isdir(LOG_PATH):
            os.mkdir(LOG_PATH)

        f = logging.Formatter(
          fmt='[%(levelname)s:%(asctime)s.%(msecs)d '
              '%(filename)s->%(funcName)s{%(lineno)d}] '
              '%(message)s',
          datefmt='%Y%m%d_%H%M%S'
        )

        log_time = time.strftime("%Y%m%d_%H%M%S",
                time.localtime(time.time()))

        handlers = [
          logging.handlers.RotatingFileHandler(
            LOG_PATH + '/Core_{0}.log'.format(log_time),
            encoding='utf8',
            maxBytes=4194304,
            backupCount=9),
          logging.StreamHandler()
        ]

        self.root_logger = ColoredLogging('colored')
        self.root_logger.setLevel(logging_level)

        for handler in handlers:
            handler.setFormatter(f)
            handler.setLevel(logging_level)
            self.root_logger.addHandler(handler)
