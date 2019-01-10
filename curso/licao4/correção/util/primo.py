def crivo(n):
    lprimos=[]
    for x in range(2,(n+1)):
        lprimos.append(x)
    p = 2;
    while p**2<=n:
        m = 2;
        while (m*p <= n):
            for i in range(len(lprimos)):
                valor = lprimos[i];
                if valor==(m*p):
                    lprimos.remove(valor)
                    break
            m=m+1
        i=lprimos.index(p)
        if i+1<(n+1):
            p=lprimos[i+1]  
    return lprimos
    