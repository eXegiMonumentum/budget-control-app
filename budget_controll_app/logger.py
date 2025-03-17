
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # DEBUG

file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.ERROR)  # ERROR, CRITICAL (writes to file)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # INFO, WARNING, ERROR, CRITICAL (writes in  console)

formatter = logging.Formatter('%(asctime)s - %(module)s - %(name)s - %(levelname)s - %(message)s - Line: %(lineno)d')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)
