import logging
from log4mongo.handlers import MongoHandler

# Create a custom logger
logger = logging.getLogger('app')
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler('app_logs.log')
# mongo_handler = MongoHandler(host='localhost')
console_handler.setLevel(logging.DEBUG)
file_handler.setLevel(logging.DEBUG)
# mongo_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# mongo_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)
# mongo_handler.setFormatter(mongo_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)
# logger.addHandler(mongo_handler)