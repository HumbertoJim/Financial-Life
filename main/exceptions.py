class NotAuthenticated(Exception):
    def __init__(self, mensaje='Not authenticated'):
        self.mensaje = mensaje
        super().__init__(self.mensaje)

class DuplicatedValue(Exception):
    def __init__(self, mensaje='Duplicated value'):
        self.mensaje = mensaje
        super().__init__(self.mensaje)