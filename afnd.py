import pydot
import os
os.environ["PATH"] +=os.pathsep + "C:\\Program Files (x86)\\Graphviz\\bin"
dir_path = os.path.dirname(os.path.realpath(__file__))

class estado:
    def __init__(self):
        self.name = None
        self.proxEstado = None
        self.anteriorEstado = None

    def get_proxEstado(self):
        return self.proxEstado
    
    def set_proxEstado(self, prox):
        self.proxEstado = prox

    def get_anteriorEstado(self):
        return self.anteriorEstado
    
    def set_anteriorEstado(self, anterior):
        self.anteriorEstado = anterior

class Automato:
    def __init__(self):
        self.alfabeto = []
        self.transicoes = {}
        self.estados = []
        self.estadoInicial = None
        self.estadosFinais = []
        self.primeiro_estado = None
        self.ultimo_estado = None
        self.quantidade_estados = 0
        
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
        self.alfabeto.append("lambda")
    
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
                        for i in transicoes[estado][entrada]:
                            if(i not in self.estados):
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
            print("Funções de transições fora do Padrao de um AFND")

    def laco_transicoes(self,simbolo):
        estado = self.primeiro_estado
        aux_inicio = None
        aux_fim = None
        #if estado != None:
        while estado.get_proxEstado() != None:
            self.criaGrafo(estado,simbolo,"red")
            aux1, aux2 = self.aplicacao_transicoes(simbolo, estado)            
            if((aux_inicio and aux_inicio) == None):
                aux_inicio = aux1
                aux_fim = aux2
            else:
                aux_fim.set_proxEstado(aux1)
                if aux1 != None:
                    aux1.set_anteriorEstado(aux_fim)
                    aux_fim = aux2
            estado = estado.get_proxEstado()
            if(estado == None):
                break
            
        else:
            
            self.criaGrafo(estado,simbolo,"green")
            aux1, aux2 = self.aplicacao_transicoes(simbolo, estado)
            if((aux1 and aux2) != None):
                if((aux_inicio and aux_fim) == None):
                    aux_inicio = aux1
                    aux_fim = aux2
                else:
                    aux_fim.set_proxEstado(aux1)
                    aux1.set_anteriorEstado(aux_fim)
                    aux_fim = aux2
        
        if((aux_inicio and aux_fim) != None):
            estado.set_proxEstado(aux_inicio)
            aux_inicio.set_anteriorEstado(estado)
            self.ultimo_estado = aux_fim    
    def organicacao_lambda(self, estado, inicio_fila, fim_fila):
        if((inicio_fila and fim_fila) == None):
            inicio_fila = estado
            fim_fila = estado
        else:
            fim_fila.set_proxEstado(estado)
            estado.set_anteriorEstado(fim_fila)
            estado.set_anteriorEstado(fim_fila)
            fim_fila = estado
        return inicio_fila,fim_fila


    def transicao_lambda(self,estado_atual):
        inicio_fila = None
        fim_fila = None
        controle = False
        for i in range(len(self.transicoes[estado_atual]["lambda"])):
            novoEstado = estado()
            novoEstado.name = self.transicoes[estado_atual]["lambda"][i]
            if(i == len(self.transicoes[estado_atual]["lambda"])):
                controle = True
            while(self.transicoes[novoEstado.name]["lambda"] != []):
                guarda_estado = novoEstado.name
                for j in range(len(self.transicoes[novoEstado.name]["lambda"])):
                    if(j>0):
                        newEstado = estado()
                        newEstado.name = self.transicoes[guarda_estado]["lambda"][j]
                        inicio_fila, fim_fila = self.organicacao_lambda(newEstado,inicio_fila,fim_fila)
                    else:
                        novoEstado.name = self.transicoes[novoEstado.name]["lambda"][j]
                        #print(novoEstado.name)
                        inicio_fila, fim_fila = self.organicacao_lambda(novoEstado,inicio_fila,fim_fila)
                    self.quantidade_estados += 1
            else:
                if(controle == False):
                    inicio_fila, fim_fila = self.organicacao_lambda(novoEstado,inicio_fila,fim_fila)
                    self.quantidade_estados += 1
        return inicio_fila,fim_fila
 
    def aplicacao_transicoes(self, simbolo,estado_atual):    
        aux_inicio = None
        aux_fim = None
        estados = estado_atual.name
        
        for i in range(len(self.transicoes[estados][simbolo])):
            if(i == 0):
                estado_atual.name = self.transicoes[estados][simbolo][i]
                inicio_lambda, fim_lambda = self.transicao_lambda(estado_atual.name) 
                if((aux_inicio and aux_fim) == None):
                    aux_inicio = inicio_lambda
                    aux_fim = fim_lambda
                else:  
                    print(inicio_lambda.name, fim_lambda.name)
                    aux_fim.set_proxEstado(inicio_lambda)
                    inicio_lambda.set_anteriorEstado(aux_fim)
                    aux_fim =fim_lambda
            else:
                novoEstado = estado()
                novoEstado.name = self.transicoes[estados][simbolo][i]
                inicio_lambda, fim_lambda = self.transicao_lambda(novoEstado.name)
                if((aux_inicio and aux_fim) == None):
                    aux_inicio = novoEstado
                    aux_fim = novoEstado
                else:
                    aux_fim.set_proxEstado(novoEstado)
                    novoEstado.set_anteriorEstado(aux_fim)
                    aux_fim = novoEstado
                if((inicio_lambda and fim_lambda) != None):
                    aux_fim.set_proxEstado(inicio_lambda)
                    inicio_lambda.set_anteriorEstado(aux_fim)
                    aux_fim =fim_lambda

                self.quantidade_estados += 1
        if(len(self.transicoes[estados][simbolo]) == 0):
            self.entrada_sem_saida(estado_atual)
        return aux_inicio, aux_fim

    def entrada_sem_saida(self, estado):
        if(estado == self.primeiro_estado):
            self.primeiro_estado = self.primeiro_estado.get_proxEstado()
        elif(estado == self.ultimo_estado):
            self.ultimo_estado = self.ultimo_estado.get_anteriorEstado()
            self.ultimo_estado.set_proxEstado(None)
        else:
            estado1 = estado.get_anteriorEstado()
            estado2 = estado.get_proxEstado()
            estado1.set_proxEstado(estado2)
            estado2.set_anteriorEstado(estado1)
        self.quantidade_estados += -1

    def set_string(self, string):
        self.faltaLer.extend(string)
        self.palavraCompleta=string

        for simbolo in list(set(string)):
            if(simbolo not in self.alfabeto):
                print("'"+ simbolo +"' nao faz parte do alfabeto")
                return
            
        if(self.quantidade_estados == 0):
            if(self.estadoInicial == None):
                print("Automato não possui estado inicial")
                return
            novoEstado = estado()
            novoEstado.name = self.estadoInicial
            self.primeiro_estado = novoEstado
            self.ultimo_estado = novoEstado
            self.quantidade_estados += 1

        for simbolo in string:
            self.laco_transicoes(simbolo)   
        estado_atual = self.primeiro_estado

        if(estado_atual != None):
            while(estado_atual.get_proxEstado() != None):
                if(self.verificacao_automato(estado_atual.name) == True):
                    self.end()
                    return True
                estado_atual = estado_atual.get_proxEstado()
            else:
                if(self.verificacao_automato(estado_atual.name) == True):
                    self.end()
                    return True
                else:
                    print("String Recusada")
                    os.system("copy .\\image\\zrejeitada.jpg .\\temp")
                    self.end()
                    return False
        else:
            print("String Recusada")            
            os.system("copy .\\image\\zrejeitada.jpg .\\temp")
            self.end()
            return False
        
    def verificacao_automato(self, estado):
        if(estado in self.estadosFinais):
            print("String Aceita")
            os.system("copy .\\image\\zaceita.jpg .\\temp")
            return True

    def end(self):
        self.primeiro_estado = None
        self.ultimo_estado = None
        self.quantidade_estados = 0

    
    def criaGrafo(self,estadoAtual,simbolo,cor):
        if(simbolo=="lambda"):
            simbolo = u'\u03BB'
        txt = "Palavra a testar: "+ self.palavraCompleta+ "\n lendo " + simbolo
        #self.faltaLer.remove(simbolo)
        self.jaLeu.append(simbolo)
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
                if entrada =="episilon":
                    entrada = u'\u03BB'
                #print("n: ", n, " estadoAtual: ",estadoAtual, " entrada: ",entrada," simbolo: ",simbolo)
                if n == estadoAtual.name and entrada == simbolo:
                    if n in self.estadoInicial:
                        my_node = pydot.Node(n, label=n, shape="invtriangle",color=cor)
                    elif n in self.estadosFinais:
                        my_node = pydot.Node(n, label=n, shape="doublecircle", color=cor)
                    else:
                        my_node = pydot.Node(n, label=n, shape="circle", color=cor)
                    for x in self.transicoes[n][entrada]:
                        config = pydot.Edge(n,x,  color=cor, label=" "+entrada, arrowhead='vee')
                        graph.add_edge(config)
                 
                else:
                
                    for x in self.transicoes[n][entrada]:
                        
                        config = pydot.Edge(n, x,  color='black', label=" "+entrada, arrowhead='vee')
                        graph.add_edge(config)
                #print(self.transicoes[n][entrada])
                
            graph.add_node(my_node)
            
        graph.write_jpg(".\\temp\\"+str(cor)+str(''.join(self.jaLeu))+".jpg")
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