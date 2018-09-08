import math

class Metodos:

    def __init__(self):
        '''
        Constructor
        '''
    ## só para testar:.
    def func(x):
        f = float(x**2 + x - 6)
        """""
        OBS: para essa função a raiz se encontra no ponto 1.999...
        """""
        return f
    
    def funcaoSecante(x):
        f = float(x**3 - (13 * x) - 12)
        return f



    def falsaposicao(self, a, b, tol, Ni):
        #Verificando se f(a)f(b)<0:.
        fa = func(a)
        fb = func(b)
        condicao = fa * fb
        
        #VERIFICA SE a e b tem sinais 
        if(condicao > 0):
            raise ValueError('A funcao deve ter sinais opostos em a e b!')
        
        x0 = ( (a * fb) - (b * fa) ) / (fb - fa)
        fx0 = func(x0)
            
        if( (fa * fx0) < 0 ):
            b = x0
        elif( (fa * fx0) > 0 ):
            a = x0
        
        erro = 10
        done = 0
        i = 2
        Ni -= 1
        print("(i = {0:d}) f(xm)={1:f} | f(a)={2:f} | f(b)={3:f} | xm={4:f}".format(1,fx0,fa,fb, x0))
        
        while( (erro > tol) and (not done) and (Ni != 0) ):
            
            #Verificando se f(a)f(b)<0:.
            fa = func(a)
            fb = func(b)
            condicao = fa * fb
            
            if(condicao < 0):
                xm = ( (a * fb) - (b * fa) ) / (fb - fa)
                fxm = func(xm)
                
                print("(i = {0:d}) f(xm)={1:f} | f(a)={2:f} | f(b)={3:f} | xm={4:f}".format(i,fxm,fa,fb,xm))
                
                if( (fa * fxm) < 0 ):
                    b = xm
                elif( (fa * fxm) > 0 ):
                    a = xm
                else:
                    done = 1 
            
            erro = ((xm - x0) / xm)
            Ni = Ni - 1
            i = i + 1
        
        print("Solucao encontrada: {0:f}".format(xm))


    def secante(self, x0, x1, tol, Ni):

        #VARIÁVEIS
        erro = 10 
        i = 1
        fx0 = 0
        fx1 = 0
        xn = 0
        
        while( (erro > tol) and (i <= Ni) ):
            
            # Calculando a f(x0) e f(x1):.
            fx0 = func(x0)
            fx1 = func(x1)
            
            xn = ( ( (x0 * fx1) - (x1 * fx0) ) / (fx1 - fx0) )
            
            print("(i = {0:d}) | x{0:d}={1:f}".format(i,xn))
            
            erro = abs(xn - x1)
    
            x0 = x1
            x1 = xn
            
            i += 1
            
        print("Solucao encontrada: {0:f}".format(xn))
        
    def muller(self, x0, x1, x2, tol, Ni):
        
        #variaveis:
        i = 1
        ER = 100
        
        while( (ER > tol) and (i <= Ni) ):
            
            ## Avaliamos a Função nas estimativas
            fx0 = funcaoSecante(x0)
            fx1 = funcaoSecante(x1)
            fx2 = funcaoSecante(x2)
            
            ## Calculamos h0, h1, sigma0, sigma1
            h0 = x1 - x0
            h1 = x2 - x1
            sigma0 = (fx1 - fx0) / (x1 - x0)
            sigma1 = (fx2 - fx1) / (x2 - x1)
            
            ## Calculamos a, b, c
            a = (sigma1 - sigma0) / (h1 + h0)
            b = (a * h1) + sigma1
            c = fx2
            
            ## Calculamos o Xn:.
            if( abs(b + math.sqrt(b**2 - (4 * a * c) ) ) > abs(b - math.sqrt(b**2 - (4 * a * c) ) ) ):
                xn = x2 + ( (-2 * c) / (b + math.sqrt(b**2 - (4 * a * c) ) ) )
            else:
                xn = x2 + ( (-2 * c) / (b - math.sqrt(b**2 - (4 * a * c) ) ) )
                
            ## Calculamos o erro relativo:.
            ER = ( abs(xn - x2) / abs(xn) ) * 100    
            
            ## Print do resultado:.
            print("(i = {0:d}) | x{0:d}={1:f} | ER = {2:f}".format(i, xn, ER))
                
            ## atualizamos os valores:.
            x0 = x1
            x1 = x2
            x2 = xn
            
            ## Incermenta i++
            i += 1
        
    
