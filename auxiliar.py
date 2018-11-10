from graphviz import Graph
class Tree:
    def __init__(self, typeNode='', child=[], value=''):
        self.type = typeNode
        self.child = child
        self.value = value

    def __str__(self):
        return self.type

def printArvore(no, esp='| ', i=0):
    
    if(not no):
        return
    
    print(esp, no.type, no.value)
    
    for filho in no.child:
        printArvore(filho, esp + '| ',i+1)

def desenhagrafico(node, grafico,i=0):
    if(not node):
        return

    pai = str(id(node))
    grafico.node(pai, node.type)
    
    for son in node.child:
        filho = str(id(son))
        grafico.node(filho, son.type)
        grafico.edge(pai, filho)

        if(son.value):
            neto = str(id(pai) + id(son) + id(son.value)) + str(i)
            grafico.node(neto, str(son.value))
            grafico.edge(filho, neto)
        desenhagrafico(son, grafico,i+1)

def geraArvoreGraph(no, Erros, bol):
    if(bol):
        if not Erros :
            printArvore(no)
            if(no) :
                grafico = Graph('G', filename='Tree.gv', strict=True)
                desenhagrafico(no, grafico)
                grafico.node_attr.update(color='lightblue2', style='filled')
                grafico.view()

