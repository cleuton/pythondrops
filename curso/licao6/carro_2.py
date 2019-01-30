class Carro:
    eixos = 2
    def __init__(self,marca=None):
        self.marca = marca
    @staticmethod
    def comentario():
        return "Esta é a classe carro."
    @classmethod
    def tipoVeiculo(cls):
        return "Este veículo tem {} eixos".format(cls.eixos)
