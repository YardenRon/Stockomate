from . import *

class MongoDB:

    def save_companies(self, companies):
        for company in companies:
            company.save()

