"""
Trabalho efetuado pelo aluno do curso de Sistemas de Informação do ICEA - UFOP:

Felipe Sousa Nunes - 16.1.8152

"""
from automato import Automato

def leituraDoArquivo(automato):
    f = open("arquivo.txt", "r")
    texto = []
    linhas = f.read().splitlines()
    for x in linhas:
        texto.append(x.split(" "))
    print(texto)
    primeiraLinha = texto[0]
    ultimaLinha = texto[len(texto)-1]
    texto.remove(ultimaLinha)
    texto.remove(primeiraLinha)

    print("primeiraLinha: ",primeiraLinha)
    print("ultima linha: ", ultimaLinha)
    print("meio: ",texto)
  
    estadoFinal = [] 
    transicoes = {}
    alfabeto = []
    palavra = []
    estados = []

    separador = primeiraLinha.index(";")
    for x in primeiraLinha:
        if(primeiraLinha.index(x)<separador):
            estadoInicial=x
        if(primeiraLinha.index(x)>separador):
            estadoFinal.append(x)

    palavra = ultimaLinha[len(ultimaLinha) - 1]
    print("estado inicial: ",estadoInicial)
    print("estado final: ", estadoFinal)
    print("palavra: ", palavra)

    
    dicEntradas = {}
    for x in texto:
        
        dicEntradas[x[1]] = x[3]
        transicoes[x[0]] = dict(dicEntradas)
        if x[0] not in estados:
            estados.append(x[0])
        if x[1] not in alfabeto:
            alfabeto.append(x[1])

    print("\n\nestados: ", estados)
    print("transicoes: ",transicoes)
    print("alfabeto: ", alfabeto)

    automato.set_alfabeto(alfabeto)
    automato.set_estados(estados)
    automato.set_estadoInicial(estadoInicial)
    automato.set_estadosFinais(estadoFinal)
    automato.set_transicoes(transicoes)
    automato.set_string(palavra)

    return automato


def main():
    fnd = Automato()
    leituraDoArquivo(fnd)
    


if __name__ == '__main__':
    main()