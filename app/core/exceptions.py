class MyError(Exception):
    def __init__(self, code, message="Возникла ошибка"):
        self.code = code
        self.message = message
        super().__init__(self.message)