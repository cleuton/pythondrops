import math

def calc_delta(a,b,c):
    delta = b**2 - 4 * a * c 
    return delta
    
a = float(input("a: "))
b = float(input("b: "))
c = float(input("c: "))

delta = calc_delta(a, b, c)

if delta > 0:
    x1 = (-b + math.sqrt(delta)) / (2*a)
    x2 = (-b - math.sqrt(delta)) / (2*a)
    print(f"x1: {x1} e x2: {x2}")
elif delta == 0:
    x = (-b + math.sqrt(delta)) / (2*a)
    print(f"x: {x}")
else:
    print("Não possui raízes reais")
