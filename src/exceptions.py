class ApiException(Exception):
    def __init__(self, msg=None, code=404, param=None):
        super().__init__()
        self.msg = msg
        if msg is None:
            self.msg = 'Something went wrong'

        self.code = code
        self.param = param

    def __str__(self):
        return f'Error {self.code} - {self.msg}'
