
import re
import math

import Metodos

if __name__ == '__main__':

    funcoesMatematicas = ['log', 'sen', 'cos', 'tan', 'sqrt']

    ###
    # Este metodo substitui qualquer variavel por um valor em uma funcao!
    # 
    # Retorno: Um string pra ser usado como funcao
    ###
    def funcao(funcao, valor):
        listaFuncao = list()
        exprecao = ''

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
            exprecao += token


        return exprecao

    ###
    # Este metodo calcula uma exprecao dada em string
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
    # Retorno: Um numero real com o resultado da exprecao
    ###
    def calcula_exprecao(exprecao):
        resultado = 0
        termo = ''
        termoFinal = ''

        listaElementos = re.split(r'(\(|\)|\^|\+|\*|\/|\-)', exprecao)

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

    def calcula_termo(termo):
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

    #Exemplo de execucao:
    print calcula_exprecao(funcao('(2+euler+4)*(7*x/sqrt(3*43))/cos(x)+sen(log(10))', '20'))
