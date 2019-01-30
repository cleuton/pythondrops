class Veiculo:
    rodas = 4
    __contagem = 100
    def __init__(self,marca=None):
        self.marca = marca
    @classmethod
    def quemSou(cls):
        return(cls)
    def mostrar(self):
        return {'marca': self.marca}

class Carro(Veiculo):
    __contagem = 50

