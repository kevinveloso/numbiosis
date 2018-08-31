class Metodos:

    def __init__(self):
        '''
        Constructor
        '''


    def falsaposicao(self, a, b, tol, Ni):
        #Verificando se f(a)f(b)<0:.
        fa = f(a)
        fb = f(b)
        condicao = fa * fb
        
        #VERIFICA SE a e b tem sinais 
        if(condicao > 0):
            raise ValueError('A funcao deve ter sinais opostos em a e b!')
        
        x0 = ( (a * fb) - (b * fa) ) / (fb - fa)
        fx0 = f(x0)
            
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
            fa = f(a)
            fb = f(b)
            condicao = fa * fb
            
            if(condicao < 0):
                xm = ( (a * fb) - (b * fa) ) / (fb - fa)
                fxm = f(xm)
                
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

    def secante(self):
        print 'secante'
    def muller(self):
        print 'muller'
