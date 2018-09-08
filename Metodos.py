import re
import math

class Metodos:

    funcoesMatematicas = ['log', 'sen', 'cos', 'tan', 'sqrt']

    def __init__(self, funcao):
        self.funcao = funcao

    def setFuncao(self, funcao):
        self.funcao = funcao

    ###
    # Este metodo substitui qualquer variavel por um valor em uma funcao!
    #
    # Retorno: Um string pra ser usado como funcao
    ###
    def funcaoSub(self, funcao, valor):
        listaFuncao = list()
        expressao = ''

        ### SUBSTITUINDO A VARIAVEL PELO VALOR ###

        #Dividindo por tudo que nao eh letra
        listaFuncao = re.split(r'([^a-z])', funcao)

        #Removendo as strings vazias
        for token in listaFuncao:
            if token == '':
                listaFuncao.remove(token)
            elif re.match(r'([a-z])', token) and len(token) == 1:
                listaFuncao[listaFuncao.index(token)] = valor

        #Transformando a funcao de volta numa string
        for token in listaFuncao:
            expressao += token


        return expressao

    ###
    # Este metodo calcula uma expressao dada em string
    #
    # AS SEGUINTE FUNCOES MATEMATICAS DEVEM SER ESCRITAS POR:
    #   raiz quadrada: sqrt(x)
    #   log na base 10: log(x)
    #   seno: sen(x)
    #   cosseno: cos(x)
    #   tangente: tan(x)
    #
    # AS SEGUINTES CONSTANTES MATEMATICAS DEVEM SER ESCRITAS POR:
    #   e: euler
    #   pi: pi
    #
    # Retorno: Um numero real com o resultado da expressao
    ###
    def calcula_expressao(self, expressao):
        resultado = 0
        termo = ''
        termoFinal = ''

        listaElementos = re.split(r'(\(|\)|\^|\+|\*|\/|\-)', expressao)

        #Remove espacos em branco criados no split
        for elemento in listaElementos:
            if elemento == '':
                listaElementos.remove(elemento)


        #Substitui as constantes: euler e pi
        index = 0
        while index < len(listaElementos):

            if listaElementos[index] == 'euler':
                listaElementos[index] = math.e
            elif listaElementos[index] == 'pi':
                listaElementos[index] = math.pi

            index += 1

        indexAbertura = 0 #Indice do ultimo parenteses aberto
        index = 0
        while index < len(listaElementos):
            if listaElementos[index] == '(':
                termo = ''
                indexAbertura = index

                index += 1
            elif listaElementos[index] == ')':
                listaElementos[indexAbertura] = calcula_termo(termo) #Coloca o resultado no lugar da abertura do parenteses
                termo = ''

                #Apaga todos os elementos da abertura ate o fechamento do parenteses
                k = indexAbertura + 1
                indexRemovido = k
                while k <= index:
                    del listaElementos[indexRemovido]
                    k += 1
                index = 0
            else:
                termo += str(listaElementos[index])
                index += 1

        for elemento in listaElementos:
            termoFinal += str(elemento)

        resultado = calcula_termo(termoFinal)

        return resultado

    def calcula_termo(self, termo):
        resultado = 0
        listaElementos = re.split(r'(\+|\*|\/|\-)', termo)

        #Remove espacos em branco criados no split
        for elemento in listaElementos:
            if elemento == '':
                listaElementos.remove(elemento)

        #Resolve os elementos logaritmos, senos, cosenos e tangentes
        index = 0
        while index < len(listaElementos):

            if listaElementos[index][:3] == 'log':
                numero = re.findall(r'[0-9]+\.[0-9]+|[0-9]+', listaElementos[index]) #Retorna uma lista com o numero dentro da string
                listaElementos[index] = math.log10(float(numero[0]))

            elif listaElementos[index][:3] == 'sen':
                numero = re.findall(r'[0-9]+\.[0-9]+|[0-9]+', listaElementos[index]) #Retorna uma lista com o numero dentro da string
                listaElementos[index] = math.sin(float(numero[0]))

            elif listaElementos[index][:3] == 'cos':
                numero = re.findall(r'[0-9]+\.[0-9]+|[0-9]+', listaElementos[index]) #Retorna uma lista com o numero dentro da string
                listaElementos[index] = math.cos(float(numero[0]))

            elif listaElementos[index][:3] == 'tan':
                numero = re.findall(r'[0-9]+\.[0-9]+|[0-9]+', listaElementos[index]) #Retorna uma lista com o numero dentro da string
                listaElementos[index] = math.tan(float(numero[0]))

            elif listaElementos[index][:4] == 'sqrt':
                numero = re.findall(r'[0-9]+\.[0-9]+|[0-9]+', listaElementos[index]) #Retorna uma lista com o numero dentro da string
                listaElementos[index] = math.sqrt(float(numero[0]))

            index += 1

        #Calcula os exponenciais
        index = 0
        while index < len(listaElementos):

            if listaElementos[index] == '^':
                listaElementos[index - 1] = pow(float(listaElementos[index - 1]), int(listaElementos[index + 1]))
                del listaElementos[index + 1]
                del listaElementos[index]
                index -= 1
            else:
                index += 1

        #Calcula as multiplicacoes e as divisoes
        index = 0
        while index < len(listaElementos):

            if listaElementos[index] == '*':
                listaElementos[index - 1] = float(listaElementos[index - 1]) * float(listaElementos[index + 1])
                del listaElementos[index + 1]
                del listaElementos[index]
                index -= 1

            elif listaElementos[index] == '/':
                listaElementos[index - 1] = float(listaElementos[index - 1]) / float(listaElementos[index + 1])
                del listaElementos[index + 1]
                del listaElementos[index]
                index -= 1
            else:
                index += 1

        #Calcula as adicoes e as subtracoes
        index = 0
        while index < len(listaElementos):

            if listaElementos[index] == '+':
                listaElementos[index - 1] = float(listaElementos[index - 1]) + float(listaElementos[index + 1])
                del listaElementos[index + 1]
                del listaElementos[index]
                index -= 1

            elif listaElementos[index] == '-':
                listaElementos[index - 1] = float(listaElementos[index - 1]) - float(listaElementos[index + 1])
                del listaElementos[index + 1]
                del listaElementos[index]
                index -= 1

            else:
                index += 1

        resultado = listaElementos[0]

        return resultado

    def funcaoSecante(self, x):
        f = float(x**3 - (13 * x) - 12)
        return f



    def falsaposicao(self, a, b, tol, Ni):
        #Verificando se f(a)f(b)<0:.
        fa = self.calcula_expressao(self.funcaoSub(self.funcao, str(a)))
        fb = self.calcula_expressao(self.funcaoSub(self.funcao, str(b)))
        condicao = fa * fb

        #VERIFICA SE a e b tem sinais
        if(condicao > 0):
            raise ValueError('A funcao deve ter sinais opostos em a e b!')

        x0 = ( (a * fb) - (b * fa) ) / (fb - fa)
        fx0 = self.calcula_expressao(self.funcaoSub(self.funcao, str(x0)))

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
            fa = self.calcula_expressao(self.funcaoSub(self.funcao, str(a)))
            fb = self.calcula_expressao(self.funcaoSub(self.funcao, str(b)))
            condicao = fa * fb

            if(condicao < 0):
                xm = ( (a * fb) - (b * fa) ) / (fb - fa)
                fxm = self.calcula_expressao(self.funcaoSub(self.funcao, str(xm)))

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
            fx0 = self.calcula_expressao(self.funcaoSub(self.funcao, str(x0)))
            fx1 = self.calcula_expressao(self.funcaoSub(self.funcao, str(x1)))

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
            fx0 = self.calcula_expressao(self.funcaoSub(self.funcao, str(x0)))
            fx1 = self.calcula_expressao(self.funcaoSub(self.funcao, str(x1)))
            fx2 = self.calcula_expressao(self.funcaoSub(self.funcao, str(x2)))

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
