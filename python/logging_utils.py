'''Configure logging for FCCAnalyses command-line entry points.'''

import logging
import sys


class _MultiLineFormatter(logging.Formatter):
    '''Align continuation lines with the start of the message.'''

    def format(self, record: logging.LogRecord) -> str:
        header = super().format(logging.LogRecord(
            name=record.name,
            level=record.levelno,
            pathname=record.pathname,
            lineno=record.lineno,
            msg='', args=(), exc_info=None,
        ))
        head, *trailing = super().format(record).splitlines(keepends=True)
        return head + ''.join(' ' * len(header) + line for line in trailing)


def configure_logging(level: int = logging.INFO) -> None:
    '''Send messages below WARNING to stdout and warnings and errors to stderr.'''
    logger = logging.getLogger('FCCAnalyses')
    logger.setLevel(level)
    formatter = _MultiLineFormatter('----> %(levelname)s: %(message)s')

    stdout = logging.StreamHandler(sys.stdout)
    stdout.setLevel(level)
    stdout.addFilter(lambda record: record.levelno < logging.WARNING)
    stdout.setFormatter(formatter)
    logger.addHandler(stdout)

    stderr = logging.StreamHandler(sys.stderr)
    stderr.setLevel(logging.WARNING)
    stderr.setFormatter(formatter)
    logger.addHandler(stderr)
