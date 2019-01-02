from model.labirinto import Labirinto
from solver import Solver

labirinto = Labirinto(5,50)
print(labirinto)

solver = Solver()
solver.solve(labirinto)
print(labirinto)