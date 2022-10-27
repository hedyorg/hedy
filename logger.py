import logging

LOG_FORMAT = '[%(asctime)s] %(filename)s %(funcName)s %(lineno)d <%(levelname)s>: %(message)s'
logging.basicConfig(format=LOG_FORMAT)

app_logger = logging.getLogger('app')
log_queue_logger = logging.getLogger('querylog')
jsonbin_logger = logging.getLogger('jsonbin')

for _logger in (app_logger, log_queue_logger, jsonbin_logger):
    _logger.setLevel(logging.DEBUG)
