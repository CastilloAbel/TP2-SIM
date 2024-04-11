import random
import math
def uniforme(a:int, b:int)->float:
    return round(a + random.uniform(0,1) * (b-a), 4)

def exponencial(lamb:float)->float:
    return round((-1 / lamb) * math.log(1 - random.uniform(0,1)), 4)

def normal_convolucion(k:int)->float:
    x = 0
    for i in range(k):
        x += random.uniform(0,1)
    return round((x - k/2) / math.sqrt(k/12), 4)


def generar_serie(n:int)->list:
    pass


def main():
    x = uniforme(8, 14)
    y = exponencial(0.01)
    z = normal_convolucion(12)
    print(z)

if __name__ == "__main__":
    main()