class Veiculo():
    rodas = 4
    def __init__(self, marca=None):
        self.marca = marca

class Automotor():
    cilindradas = 1000

class Carro(Veiculo,Automotor):
    def mostrar(self):
        return {'marca':self.marca, 'cilindradas':self.cilindradas}
