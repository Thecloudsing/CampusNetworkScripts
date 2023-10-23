import logging
from colorlog import ColoredFormatter


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
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
logging.root.setLevel(LOG_LEVEL)
formatter = CustomizationFormatter(
    fmt=LOG_FORMAT,
    datefmt=DATE_FORMAT
)

stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)

log = logging.getLogger('root')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)
