from utils import logger

class MissingDataError(Exception):

    def __init__(self, company_id, company_name, missing_data):
        self.id = company_id
        self.name = company_name
        self.missing_data = missing_data

    def __str__(self):
        message = "MissingDataError: company id={}, company name={}, missing data={}"\
            .format(self.id, self.name, self.missing_data)
        logger.exception(message)
        return message