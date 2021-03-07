import pydot
import os
os.environ["PATH"] +=os.pathsep + "C:\\Program Files (x86)\\Graphviz\\bin"
dir_path = os.path.dirname(os.path.realpath(__file__))

class Automato:
    def __init__(self):
        self.alfabeto = []
        self.transicoes = {}
        self.estados = []
        self.estadoInicial = None
        self.estadosFinais = []
        self.count=0
        self.faltaLer = []
        self.jaLeu = []
        self.palavraCompleta = ''
    
    def verificar_repitidos(self, dados):
        vetor = []
        for i in dados:
            if(i not in vetor):
                vetor.append(i)
        return vetor

    def set_alfabeto(self, alfabeto):
        self.alfabeto = self.verificar_repitidos(alfabeto)

    def set_estados(self, estados):
        self.estados = self.verificar_repitidos(estados)
        self.estados.sort()
    
    def set_estadoInicial(self, estado):
        if estado in self.estados:
            self.estadoInicial = estado
        else:
            print("Estado inicial invalido")
    
    def set_estadosFinais(self, estados):
        estados = self.verificar_repitidos(estados)
        for i in estados:
            if i in self.estados:
                if i not in self.estadosFinais:
                    self.estadosFinais.append(i)
        #print(self.estadosFinais)
    
    def verificar_transicoes(self, transicoes):
        estados_transições = []

        for estado in transicoes:
            check_estados = []; estados_transições.append(estado)
            if(estado not in check_estados and estado in self.estados):
                check_estados.append(estado); check_alfabeto = []
                for entrada in transicoes[estado]:
                    check_alfabeto.append(entrada)
                    if(entrada in self.alfabeto):
                        if(transicoes[estado][entrada] not in self.estados):
                            return False
                    else:
                        return False  
                check_alfabeto.sort()
                if(check_alfabeto != self.alfabeto):
                    return False           
            else:
                return False
        
        estados_transições.sort()
        if(estados_transições != self.estados):
            return False
        return True

    def set_transicoes(self, transicoes):
        if(self.verificar_transicoes(transicoes) == True):
            self.transicoes = transicoes
        else:
            print("Funções de transições fora do Padrao de um AFD")

    def aplicacao_transicoes(self, estado_atual,simbolo):
        
        self.criaGrafo(estado_atual,simbolo)
        estado_atual = self.transicoes[estado_atual][simbolo]
        return estado_atual

    def set_string(self, string):
        self.faltaLer.extend(string)
        self.palavraCompleta=string

        for simbolo in list(set(string)):
            if(simbolo not in self.alfabeto):
                print("'"+ simbolo +"' nao faz parte do alfabeto")
                return
            
        estado_atual = self.estadoInicial
        if(estado_atual != None):
            for simbolo in string:
                estado_atual = self.aplicacao_transicoes(estado_atual, simbolo)
        
            if(estado_atual in self.estadosFinais):
                print("String Aceita")
                os.system("copy .\\image\\aceita.jpg .\\temp")
                return True
            else:
                print("String Recusada")
                os.system("copy .\\image\\rejeitada.jpg .\\temp")
                return False
        else:
            print("Automato não possui estado inicial")

    def criaGrafo(self,estadoAtual,simbolo):
        txt = "Palavra a testar: "+ self.palavraCompleta+ "\n lendo " + simbolo
        self.faltaLer.remove(simbolo)
        self.jaLeu.append(simbolo)
        txt+= " falta: "+ ''.join(self.faltaLer)
        graph = pydot.Dot('my_graph', graph_type='digraph', bgcolor='white', label=str(txt))
        
        # Add nodes
        for n in self.estados:
            if n in self.estadoInicial:
                my_node = pydot.Node(n, label=n, shape="invtriangle")
            elif n in self.estadosFinais:
                my_node = pydot.Node(n, label=n, shape="doublecircle")
            else:
                my_node = pydot.Node(n, label=n, shape="circle")
            for entrada in self.transicoes[n]:
                #print("n: ",n," estadoAtual: ",estadoAtual," entrada:", entrada, " simbolo:",simbolo)
                if n == estadoAtual and entrada == simbolo:
                    if n in self.estadoInicial:
                        my_node = pydot.Node(n, label=n, shape="invtriangle",color="green")
                    elif n in self.estadosFinais:
                        my_node = pydot.Node(n, label=n, shape="doublecircle", color="green")
                    else:
                        my_node = pydot.Node(n, label=n, shape="circle", color="green")
                    config = pydot.Edge(n, self.transicoes[n][entrada],  color='red', label=" "+entrada, arrowhead='vee')
                    
                else:
                    config = pydot.Edge(n, self.transicoes[n][entrada],  color='black', label=" "+entrada, arrowhead='vee')
                graph.add_edge(config)
            graph.add_node(my_node)
            
        graph.write_jpg(".\\temp\\"+str(''.join(self.jaLeu))+".jpg")
       # os.startfile(str(estadoAtual)+" lendo "+str(simbolo)+".png")
        self.count+=1

    def criaGif(self):
        try:
            os.system("magick convert -delay 120 -loop 0 .\\temp\\*.jpg -resize 400x400 imagem.gif")
            os.startfile("imagem.gif")
            #Parte para apagar os arquivos da pasta temporaria
            pathAtual = dir_path+"\\temp\\"
            dir = os.listdir(pathAtual)
            for file in dir:
                os.remove(pathAtual+"\\"+file)   #deleta o file da pasta temp
        except:
            print("error ao criar o gif ou apagar os arquivos da pasta temp")