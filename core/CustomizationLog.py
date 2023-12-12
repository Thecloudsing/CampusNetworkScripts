import logging, traceback, atexit
from time import asctime, localtime, time
from colorlog import ColoredFormatter
from core.FileUtils import exists_dir

log_path = './log'
exists_dir(log_path)


class CustomizationFormatter(ColoredFormatter):
    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        funcName = record.funcName
        filename = record.filename
        record.customization_funcName = funcName if len(funcName) <= 20 else f'...{funcName[0:17]}'
        record.customization_filename = filename if len(filename) <= 10 else f'...{filename[0:7]}'
        return super().format(record)


LOG_LEVEL = logging.INFO
LOG_FORMAT = "%(log_color)s%(asctime)s  %(levelname)-10s%(process)d --- [%(customization_funcName)20s] %(filename)-10s : %(message)s%(reset)s"
FILE_LOG_FORMAT = "%(asctime)s  %(levelname)-10s%(process)d --- [%(customization_funcName)20s] %(filename)-10s : %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
logging.root.setLevel(LOG_LEVEL)
formatter = CustomizationFormatter(
    fmt=LOG_FORMAT,
    datefmt=DATE_FORMAT
)

file_handler = logging.FileHandler(f'{log_path}/run.log', mode='+a', encoding='utf8')
file_handler.setLevel(level=logging.INFO)
file_handler.setFormatter(logging.Formatter(FILE_LOG_FORMAT))

stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)

log = logging.getLogger('root')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)
log.addHandler(file_handler)

error_file = open(file=f'{log_path}/error.log', mode='+a', encoding='utf8')


def out_err():
    error_file.write(f'\n{asctime(localtime(time()))}\n')
    traceback.print_exc(file=error_file)
    error_file.flush()


def close():
    error_file.close()
    log.info('file close.')


atexit.register(close)
