class PistonException(Exception):

    status_code = 500

    def __init__(self, message=None, errors=[]):
        super(PistonException, self).__init__(message)
        self.message = message
        self.errors = errors

    def __str__(self):
        return self.message

    def __dict__(self):
        return {
            "success": False,
            "type": type(self).__name__,
            "message": self.message
        }
