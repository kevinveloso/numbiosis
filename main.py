
import re

import Metodos

if __name__ == '__main__':

    ###
    # Este metodo substitui qualquer variavel por um valor em uma funcao!
    # 
    # Retorno: Um string pra ser usado como funcao
    ###
    def funcao(funcao, valor):
        arrayFunc = list()
        exprecao = ''

        ### SUBSTITUINDO A VARIAVEL PELO VALOR ###

        arrayFunc = re.split(r'([^a-z])', funcao)
        
        #Removendo as strings vazias
        for token in arrayFunc:
            if token == '':
                arrayFunc.remove(token)
            elif re.match(r'([a-z])', token) and len(token) == 1:
                arrayFunc[arrayFunc.index(token)] = valor
        
        #Transformando a funcao de volta numa string
        for token in arrayFunc:
            exprecao += token


        return exprecao


    #Exemplo de execucao:
    print funcao('(2+x+4)*(7*x/(3*43))/cos(x)+sen(log(10))', '20')
