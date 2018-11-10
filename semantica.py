from auxiliar import geraArvoreGraph, Tree
from lex import lexer
from Yacc import parser, contemErros
import sys

tabelaSimbolo = []

def pegaVariavel(no):
    variavel = []
    vet = []
    noAux = no

    while(True):
        if(noAux.value):
            variavel.append(noAux.value)
        for son in noAux.child:
            vet.append(son)
        if(len(vet) == 0):
            break
        noAux = vet.pop(0)
    variavel.__reversed__()
    return variavel

def arrayFilho(tam,var):
    array = []
    for i in range(2,tam):
        array.append(Tree(str(var[i])))
    return array

def podaDeclaracao_variaveis(no):
    var = pegaVariavel(no)
    qtdFilhos = no.child.__len__()

    if(no.child[1].child[0].child.__len__() > 0):
        filho = arrayFilho(var.__len__(), var)
        no.child[0] = Tree(var[0])
        no.child[1] = Tree(var[1], filho)
                
    else:
        for i in range(var.__len__()):
            if(i < qtdFilhos):
                no.child[i] = Tree(var[i])
            else:
                no.child.append(Tree(var[i]))


def podaPrograma(no):
        if(no.child[0].child.__len__() < 2):
            no.child[0] = no.child[0].child[0].child[0]
    

def podaDeclaracaoFuncao(no):
    no.child[0] = Tree(no.child[0].value)
    return


def encontraElementoDivisoria(no):
    if(no.child.__len__() != 1):
        return no
    return encontraElementoDivisoria(no.child)


def podaAtribuicao(no):
    ##caso1
    
    print(pegaVariavel(no))

def podaArvore(no):
    if(not no):
        return

    if(no.type == 'programa'):
        podaPrograma(no)
    elif(no.type == 'declaracao_variaveis'):
        podaDeclaracao_variaveis(no)
    # elif(no.type == 'corpo'):
    #     podaCorpo(no)
    elif(no.type == 'atribuicao'):
       podaAtribuicao(no)
    # elif(no.type == 'declaracao_funcao'):
    #     podaDeclaracaoFuncao(no)
    



    for filho in no.child:    
        podaArvore(filho)

#########################################################teste



arq = open(sys.argv[1], 'r', encoding='utf-8')
data = arq.read()
arq.close()

result = parser.parse(data, tracking=True)

podaArvore(result)
geraArvoreGraph(result, contemErros, True)
