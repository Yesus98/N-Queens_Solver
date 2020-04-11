import random

class PSR:

    def __init__(self, dominios, restricciones):

        self.dominios = dominios
        self.restricciones = restricciones
        self.variables = list(dominios.keys())

        vecinos = {v: [] for v in self.variables}
        for v1, v2 in restricciones:
            vecinos[v1].append(v2)
            vecinos[v2].append(v1)
        self.vecinos = vecinos

def n_reinas(n):
    
    def n_reinas_restriccion(x,y):
        return lambda u,v: (abs(x-y) != abs(u-v) and u != v)

    doms = {x:list(range(1,n+1)) for x in range(1,n+1)}
    restrs = dict()
    for x in range(1,n):
        for y in range(x+1,n+1):
            restrs[(x,y)] = n_reinas_restriccion(x,y)
    return PSR(doms,restrs)

def dibuja_tablero_n_reinas(asig):

    def cadena_fila(i,asig):
        cadena="|"
        for j in range (1,n+1):
            if asig[i]==j:
                cadena += " X |"
            else:
                cadena += "   |"
        return cadena
    
    n=len(asig)
    print("+"+"-"*(4*n-1)+"+")
    for i in range(1,n):
        print(cadena_fila(i,asig))
        print("|"+"-"*(4*n-1)+"|")
    print(cadena_fila(n,asig))
    print("+"+"-"*(4*n-1)+"+")

def restriccion_arco(psr, x, y):
    if (x, y) in psr.restricciones:
        return psr.restricciones[(x, y)]
    else:
        return lambda vx, vy: psr.restricciones[(y, x)](vy, vx)

def AC3_parcial(psr,doms):
	
    cola = {(x,y) for x in doms.keys() for y in doms.keys() if x != y}

    while cola:
        (x,y) = cola.pop()
        func = restriccion_arco(psr,x,y)
        dom_previo_x = doms[x]
        mod_dom_x = False
        dom_nuevo_x = []
        for vx in dom_previo_x:
            if any(func(vx, vy) for vy in doms[y]):
                dom_nuevo_x.append(vx)
            else:
                mod_dom_x = True
        if mod_dom_x:
            doms[x] = dom_nuevo_x
            cola.update((z,x) for z in psr.vecinos[x] if z != y and z in doms.keys())
    return doms

def psr_backtracking_ac3_mrv(psr):

    def MRV(resto,dominios):
        asociado = [(len(dominios[x]),x) for x in resto]
        variable = []
        for x in asociado:
            if x[0] == min(asociado)[0]:
                variable.append(x[1])
        return random.choice(variable)

    def consistente(psr,var,val,asig):
        for x in asig:

            if (var,x) in psr.restricciones:
                if not psr.restricciones[(var,x)](val,asig[x]):
                    return False
            elif (x,var) in psr.restricciones:
                if not psr.restricciones[(x,var)](asig[x],val):
                    return False
        return True

    def psr_backtracking_rec(asig,resto):
        if resto==[]:
            return asig
        else:
            var = MRV(resto,psr.dominios)
            nuevo_resto=resto.copy()
            nuevo_resto.remove(var)
            dom_var=psr.dominios[var]
            
            for val in dom_var: 
                if consistente(psr,var,val,asig):
                    
                    asig[var]=val   
                    doms = psr.dominios.copy()
                    psr.dominios[var] = [val]
                    
                    AC3_parcial(psr,psr.dominios)
                    del psr.dominios[var]
                    
                    result= psr_backtracking_rec(asig,nuevo_resto)
                    psr.dominios = doms
                    
                    if result is not None:
                        return result
                    del asig[var]
            return None
            
    sol=psr_backtracking_rec(dict(),psr.variables)
    if sol is None:
        print("No tiene solución")
    return sol


def main():
    n = int(input("Enter problem size: "))
    dibuja_tablero_n_reinas(psr_backtracking_ac3_mrv(n_reinas(n)))

if __name__ == "__main__":
    main()