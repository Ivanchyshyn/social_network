class ApiException(Exception):
    def __init__(self, msg=None):
        super().__init__()
        self.msg = msg or 'Something went wrong'

    def __str__(self):
        return f'Error - {self.msg}'

    def __repr__(self):
        return f'ApiException({self.msg})'
