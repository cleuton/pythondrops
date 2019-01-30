class Carro:
    eixos = 2
    def __init__(self,marca=None):
        self.marca = marca
    def dict(self):
        return {'marca':self.marca}
