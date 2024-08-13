import logging
import os
from logging.config import dictConfig
from typing import Any, List

import colorlog


def skip_venv_msgs(record):
  if '\\venv\\' not in record.pathname and '\\Local\\Programs\\Python\\' not in record.pathname:
    return True
  else:
    return False


def setup_logging() -> Any:
  DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1", "t"]
  LOG_PATH = "main.log"
  loggers = {
      "default": {
          'disable_existing_loggers': False,
          "level": "DEBUG",
          "handlers": ["console"] if DEBUG else ["console", "file"]},
      'utilities': {
          'handlers': [],
          'level': 'DEBUG' if DEBUG else 'ERROR',
      },
  }

  logging_config = {
      'version': 1,
      'disable_existing_loggers': False,
      'formatters': {
          'myformatter': {
              'format': '[{levelname}][{asctime}][{pathname}][{funcName}]:{lineno}: {message}',
              # '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s',
              # {process: d} {thread: d}
              'style': '{',
              # 'datefmt': '%Y-%m-%d:%H:%M:%S',
              'datefmt': '%Y-%m-%d %H:%M:%S',
          },
          'colored': {
              '()': 'colorlog.ColoredFormatter',
              # { % (pathname)s: % (lineno)d}
              'format': "%(log_color)s%(levelname)s: %(asctime_log_color)s[%(asctime)s] %(pathname_log_color)s%(pathname)s:%(lineno_log_color)s%(lineno)d %(funcName_log_color)s%(funcName)s %(message_log_color)s%(message)s",
              'datefmt': '%Y-%m-%d %H:%M:%S',
              'log_colors': {
                  'DEBUG': 'cyan',
                  'INFO': 'green',
                  'WARNING': 'yellow',
                  'ERROR': 'red',
                  'CRITICAL': 'red,bg_white',
              },
              'secondary_log_colors': {
                  'message': {
                      'DEBUG': 'cyan',
                      'INFO': 'green',
                      'WARNING': 'bold_yellow',
                      'ERROR': 'red',
                      'CRITICAL': 'blue,bg_white',
                  },
                  'lineno': {
                      'DEBUG': 'red',
                      'INFO': 'red',
                      'WARNING': 'red',
                      'ERROR': 'red',
                      'CRITICAL': 'red,bg_white',
                  },
                  'levelname': {
                      'DEBUG': 'cyan',
                      'INFO': 'green',
                      'WARNING': 'yellow',
                      'ERROR': 'red',
                      'CRITICAL': 'red,bg_white',
                  },
                  'asctime': {
                      'DEBUG': 'yellow',
                      'INFO': 'yellow',
                      'WARNING': 'yellow',
                      'ERROR': 'yellow',
                      'CRITICAL': 'yellow,bg_white',
                  },
                  'pathname': {
                      'DEBUG': 'green',
                      'INFO': 'green',
                      'WARNING': 'green',
                      'ERROR': 'red',
                      'CRITICAL': 'green,bg_white',
                  },
                  'funcName': {
                      'DEBUG': 'purple',
                      'INFO': 'purple',
                      'WARNING': 'purple',
                      'ERROR': 'purple',
                      'CRITICAL': 'purple,bg_white',
                  },
              }
          }
      },
      'filters': {
          'skip_unreadable_posts': {
              'callback': skip_venv_msgs,
          }
      },
      'handlers': {
          'console': {
              'level': 'DEBUG',
              'class': 'colorlog.StreamHandler',
              'formatter': 'colored',
              'filters': ['skip_unreadable_posts'],
          },
          'file': {
              'level': 'DEBUG',
              'class': 'logging.FileHandler',
              'formatter': 'myformatter',
              'encoding': 'utf8',
              'filename': LOG_PATH,
              'filters': ['skip_unreadable_posts'],
          }
      },
      'root': {
          'handlers': [],
          'level': 'DEBUG' if DEBUG else 'INFO',
      },
      'loggers': loggers
  }

  dictConfig(logging_config)
