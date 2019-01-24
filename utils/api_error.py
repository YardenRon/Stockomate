class ApiError(Exception):

    def __init__(self, url, status):
        self.url = url
        self.status = status

    def __str__(self):
        return "ApiError: url={}, status={}".format(self.url, self.status)