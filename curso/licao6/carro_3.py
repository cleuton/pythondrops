class Carro:
    eixos = 2
    def __init__(self,marca=None, chassi=None):
        self._chassi = chassi
        self.marca = marca
    def _mostrar(self):
        return self._chassi

