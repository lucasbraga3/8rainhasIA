import random
import numpy as np 
import math
from timeit import default_timer as timer

found = False
foundSA = False
tabuleirobase = [0,0,0,0,0,0,0,0]
tabuleirobaseSA = [0,0,0,0,0,0,0,0]
#np.array(tabuleirobase)
#attacked = set()
visitedconfigurations = set()
visitedconfigurationsSA = set()
class PriorityQueue(object):
    def __init__(self):
        self.queue = []
 
    def __str__(self):
        return ' '.join([str(i) for i in self.queue])
 
    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0
 
    # for inserting an element in the queue
    def append(self, data):
        self.queue.append(data)
 
    # for popping an element based on Priority
    def pop(self):
        try:
            max_val = 0
            for i in range(len(self.queue)):
                if self.queue[i].heuristic< self.queue[max_val].heuristic:
                    max_val = i
            item = self.queue[max_val]
            del self.queue[max_val]
            return item
        except IndexError:
            print()
            exit()

lista = []

class Nodo:
    def __init__ (self, positions):
        self.filhos = []
        self.positions = positions
        #self.depht = 0
        #self.attacked = set()
        self.soncount = 0
        self.heuristic = self.calcblock()
        #self.valor = self.potencial()
        #self.calcblock()
    def addfilho(self,newson):
        self.filhos.append(newson)
        self.soncount = self.soncount + 1
    def calcblock(self):
        h = 0
        for i in range(0,8):
           # self.attacked.add(self.positions[i])
           # if self.positions[i] != 0:
            attacked = set()
            crossing7 = False
            crossing7minus = False
            crossing9 = False
            crossing9minus = False
            for j in range(1,8):
                
                if self.positions[i] + 7*j < 65 and self.positions[i] + 7*j > -1 and crossing7 == False: 
                    attacked.add(self.positions[i] + 7*j)
                    if (self.positions[i] + 7*j + 1)%8 == 0 or (self.positions[i] + 7*j)%8 == 0:
                        crossing7 = True
                    
                if self.positions[i] - 7*j < 65 and self.positions[i] - 7*j > -1 and crossing7minus == False: 
                    attacked.add(self.positions[i] - 7*j)
                    if (self.positions[i] - 7*j)%8 == 0 or (self.positions[i] - 7*j + 1)%8 == 0:
                        crossing7minus = True

                if self.positions[i] + 9*j < 65 and self.positions[i] + 9*j > -1 and crossing9 == False: 
                    attacked.add(self.positions[i] + 9*j)
                    if (self.positions[i] + 9*j + 1)%8 == 0 or (self.positions[i] + 9*j)%8 == 0:
                        crossing9 = True

                if self.positions[i] - 9*j < 65 and self.positions[i] - 9*j > -1 and crossing9minus == False: 
                    attacked.add(self.positions[i] - 9*j)
                    if (self.positions[i] - 9*j)%8 ==0 or (self.positions[i] - 9*j + 1)%8 == 0:
                        crossing9minus = True

                if self.positions[i] + 8*j < 65 and self.positions[i] + 8*j > -1: 
                    attacked.add(self.positions[i] + 8*j)

                if self.positions[i] - 8*j < 65 and self.positions[i] - 8*j > -1: 
                    attacked.add(self.positions[i] - 8*j)
                
            for z in range(0,8):
                #print(self.positions[z])
                if self.positions[z] in attacked and z != i:
                    h = h + 1
        h = math.trunc(h/2)
        return h

def expandir(father):
    global lista
    for i in range(0,8):
        key = i*8
        #newpositions = np.array(father.positions)     
        while key <= (i*8 + 7):
            newpositions = np.array(father.positions)
            if(key != father.positions[i]):
                newpositions[i] = key
                newpositions = tuple(newpositions)
                #visitedconfigurations.add(newpositions) 
                #visitedconfigurationsSA.add(newpositions)
                newson = Nodo(newpositions)
                if newson.heuristic<father.heuristic and newpositions not in visitedconfigurations:
                    #father.addfilho(newson)
                    lista.append(newson)
                    visitedconfigurations.add(newpositions)
            key = key + 1

def checarsolucaoHC(Nodo):
    if Nodo.heuristic == 0:
        global found
        found = True
        #print("solucao encontrada")       
    else:
        expandir(Nodo)
        global lista
    
def cria_tabuleiro(config):
    newmatrix = np.array([[0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0]])
    for i in range(0,8):
        newmatrix[i][max((config[i] - (8*i)),0)] = 1
    print(newmatrix)

def procurarsolucaoHC(lista):
    start = timer()
    while found == False and lista:
        elem = lista.pop()
        checarsolucaoHC(elem)
    end = timer()
    print("achei ou fiquei preso num maximo local")
    print(elem.positions)
    print("heuristica =", elem.heuristic)
    print("tempo:",end-start)
    cria_tabuleiro(elem.positions)

for i in range(0,8):
        key = i*8
        tabuleirobase[i] = random.randint(key,key+7)
tabuleirobase = tuple(tabuleirobase)
Raiz = Nodo(tabuleirobase) #275.83286369999405
print("tabuleiro Hill Climbing:",tabuleirobase)
print("heuristica inicial:", Raiz.heuristic)
lista.append(Raiz)
procurarsolucaoHC(lista)