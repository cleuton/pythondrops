class Veiculo():
    def ligar(self):
        raise NotImplementedError("A subclasse deve implementar este método")

class Carro(Veiculo):
    def ligar(self):
        return('ligando o carro')

class Moto(Veiculo):
    def ligar(self):
        return('ligando a moto')
        