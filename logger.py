import os
import logging

LOG_LEVEL = logging.DEBUG if not os.getenv('NO_DEBUG_MODE') else logging.INFO
LOG_FORMAT = '[%(asctime)s] %(filename)s %(funcName)s %(lineno)d <%(levelname)s>: %(message)s'
logging.basicConfig(format=LOG_FORMAT)

app_logger = logging.getLogger('app')
log_queue_logger = logging.getLogger('querylog')
jsonbin_logger = logging.getLogger('jsonbin')
hedy_content_logger = logging.getLogger('hedy_content')

for _logger in (app_logger, log_queue_logger, jsonbin_logger):
    _logger.setLevel(LOG_LEVEL)
