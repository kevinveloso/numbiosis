# -*- coding: utf-8 -*-
from Metodos import Metodos

if __name__ == '__main__':

    #Exemplo de execucao:
    test = Metodos('x^2 + x - 6')
    test.falsaposicao(1.5, 2.5, 0.005, 10)
    test.secante(1.5, 2.5, 0.005, 10)
    test.setFuncao('x^3 - x * 13 - 12')
    test.muller(1.5, 3.0, 5.5, 0.05, 10)