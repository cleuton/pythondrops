import sys
from utils.timer import Timer
from multiprocessing import Pool

def fibo(n):
    if n==0: 
        return 0
    # Second Fibonacci number is 1 
    elif n==1: 
        return 1
    else: 
        return fibo(n-1)+fibo(n-2)     

def testThread(x):
    timer1 = Timer()
    timer1.tic()
    valor = fibo(34)
    timer1.toc()
    return (valor,timer1.total_time)

if __name__ == "__main__":
    if len(sys.argv)>1:
        num_proc = int(sys.argv[1])
        pool = Pool(processes=num_proc) 
        lista = pool.map(testThread,range(num_proc))
        print(lista)
    else:
        timer1 = Timer()
        timer1.tic()
        valor = fibo(34)
        timer1.toc()
        print('Resultado: ' + str(valor) + ' segundos: ' + str(timer1.total_time))


