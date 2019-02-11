from utils import logger

class ApiError(Exception):

    def __init__(self, url, status):
        self.url = url
        self.status = status

    def __str__(self):
        message = "ApiError: url={}, status={}".format(self.url, self.status)
        logger.exception(message)
        return message