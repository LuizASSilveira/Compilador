from graphviz import Graph

class Tree:
    def __init__(self, typeNode='', child=[], value=''):
        self.type = typeNode
        self.child = child
        self.value = value

    def __str__(self):
        return self.type

# def printArvore(no, esp=''):
#         if(no):
#             print(esp, no.type, no.value)
#         for filho in no.child:
#             printArvore(filho, esp + '*')

def printArvore2(no, esp='*'):
    if(not no):
        return
    print(esp, no.type, no.value)
    # for filho in no.child:
    #     print(esp + '--', filho, filho.value)
    for filho in no.child:
        printArvore2(filho, esp + '*')

def desenhagrafico(node, grafico, i):
    if(not node):
        return

    grafico.node(node.type + str(i), node.type)
    pai = str(i)
    
    for son in node.child:
        i += 1           
        grafico.node(son.type + str(i), son.type)
        grafico.edge(node.type + pai, son.type + str(i))
        
        if(son.value):
            grafico.node(str(son.value)+str(i), str(son.value))
            grafico.edge(son.type + str(i), str(son.value)+str(i))

        desenhagrafico(son, grafico, i)


# def desenhagrafico(node, grafico, i):
#     if(not node):
#         return
#     pai = str(id(node.type))+str(i)
#     grafico.node(pai, node.type)

#     for son in node.child:
#         i+=1
#         filho = str(id(son.type))+str(i)
#         grafico.node(filho, son.type)
        
#         grafico.edge(pai,filho)
#         desenhagrafico(son, grafico, i)


def geraArvoreGraph(no):
    grafico = Graph('G', filename='Tree.gv', strict=True)
    desenhagrafico(no, grafico, i=1)
    grafico.view()

