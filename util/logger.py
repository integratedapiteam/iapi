import logging

logger = logging.getLogger('dev')
logger.setLevel(logging.INFO)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)

logger.addHandler(consoleHandler)

formatter = logging.Formatter('%(asctime)s  %(name)s  %(levelname)s: %(message)s')
consoleHandler.setFormatter(formatter)
