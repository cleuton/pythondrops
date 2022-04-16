class Carro:
    eixos = 2
    __quantidade = 0
    def __init__(self,marca=None):
        Carro._Carro__quantidade+=1
        self.marca = marca
    @classmethod
    def contagem(cls):
        return "existem {} veiculos".format(cls._Carro__quantidade)

    
