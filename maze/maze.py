from model.labirinto import Labirinto
from solver import Solver
import sys
linhas = int(sys.argv[1]) if len(sys.argv)>1 else 10
colunas = int(sys.argv[2]) if len(sys.argv)>2 else 10

labirinto = Labirinto(linhas,colunas)
print(labirinto)

solver = Solver()
solver.solve(labirinto)
print(labirinto)