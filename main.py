"""
Trabalho efetuado pelo aluno do curso de Sistemas de Informação do ICEA - UFOP:

Felipe Sousa Nunes - 16.1.8152

"""
#from automato import Automato
from afnd import Automato

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

    for x in texto:
        lista = []        
        dicEntradas = {}
       # print( " x1: ", str(x[1]), " transicoes[x[0]]: ",str(transicoes[x[0]]))
      #   and 
          #  
         #   print("entrou")
        if x[1] == '/':
            x[1] = "lambda"
            print("entrou aqui")
        if x[0] in transicoes:
            dicEntrada = transicoes[x[0]] 
            print(dicEntrada)
            if x[1] in transicoes[x[0]]:
                print("entrou no if 2")
                lista = transicoes[x[0]][x[1]]                
            lista.append(x[3])
            
            dicEntrada[x[1]] = lista
            transicoes[x[0]] = dict(dicEntrada)
        else:            
            lista.append(x[3])
            if x[1] == 'lambda':
                dicEntradas['lambda'] = [x[3]]                 
                transicoes[x[0]] = dict(dicEntradas)
            else:
                dicEntradas[x[1]] = lista
                dicEntradas['lambda'] = [] 
                transicoes[x[0]] = dict(dicEntradas)

        if x[0] not in estados:
            estados.append(x[0])
        if x[1] not in alfabeto and x[1]!="lambda":
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
    automato.criaGif()
    


def main():
    fnd = Automato()
    leituraDoArquivo(fnd)
    


if __name__ == '__main__':
    main()