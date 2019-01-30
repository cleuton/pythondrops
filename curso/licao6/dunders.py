class Carro:
    def __init__(self,marca=None,comprimento=0.0):
        self.marca = marca
        self.comprimento = comprimento
    def __eq__(self,other):
        return self.marca==other.marca
    def __lt__(self,other):
        return self.comprimento<other.comprimento

