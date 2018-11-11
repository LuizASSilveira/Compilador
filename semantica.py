from auxiliar import geraArvoreGraph, Tree
from lex import lexer
from Yacc import parser, contemErros
import sys

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

    if(no.child[1].child[0].child.__len__() == 1):
        filho = arrayFilho(var.__len__(), var)
        no.child[0] = Tree(var[0])
        no.child[1] = Tree(var[1], filho)
                
    else:
        for i in range(var.__len__()):
            if(i < qtdFilhos):
                no.child[i] = Tree(str(var[i]))
            else:
                no.child.append(Tree(str(var[i])))


def podaPrograma(no):
        if(no.child[0].child.__len__() < 2):
            no.child[0] = no.child[0].child[0].child[0]
    

def encontraFolha(no):
    if(no.child.__len__() != 1 or no.value  ):
        return no
    return encontraFolha(no.child[0])


def podaAtribuicao(no):
    if(no.child.__len__() == 0):
        no.child[0] = Tree(no.child[0].value)

    var = encontraFolha(no.child[1])
    no.child[1] = var

def podaIndice(no):
    var = encontraFolha(no.child[0])
    no.child[0] = var

def podaAcao(no):
    var = encontraFolha(no.child[0])
    no.child[0] = var

def podaCorpo(no,i=0):
    if(no.child[i].child[i].type == 'vazio'):
        no.child.pop(i)
    
    if(no.child.__len__() > 1 and no.child[i].type == 'corpo' and no.child[i].child[i].type != 'vazio'):
        aux = no.child[i].child[i+1]
        no.child[i] = no.child[i].child[i]
        no.child.insert(i+1, aux)        
        podaCorpo(no)

def expressoes(no):
    
    if(no.child.__len__() == 3 and no.child[0].child.__len__() != 3):
        no.child.append(Tree(str(no.child[1].value),[]))
        
        var1 = encontraFolha(no.child[0])
        var2 = encontraFolha(no.child[2])
        
        no.child.pop(0)
        no.child.pop(0)
        no.child.pop(0)

        no.child[0].child.append(Tree(str(var1.value)))
        no.child[0].child.append(Tree(str(var2.value)))

    else:
        no.child.append(Tree(str(no.child[1].value), []))
        
        var2 = encontraFolha(no.child[2])
        var1 = no.child.pop(0)
        no.child.pop(0)
        no.child.pop(0)
        
        no.child[0].child.append(var1)
        no.child[0].child.append(Tree(str(var2.value)))
        


def podaListaDeclaracoes(no):
    if(no.child.__len__() > 1):
        no.child[1] = no.child[1].child[0]
    else:
        no.child[0] = no.child[0].child[0]

def podaRepita(no):
    var = encontraFolha(no.child[1])
    no.child[1] = var


def podaParametro(no):
    if(no.child[0].type == 'parametro'):
        no.child[0] = no.child[0].child[0]

def podaExpressao(no, i):
    var = encontraFolha(no.child[i])
    no.child[i] = var

def listaDeclaracoes(no,i=0):
    if(no.child[i].child[i].type == 'vazio'):
        no.child.pop(i)

    if(no.child.__len__() > 1 and no.child[i].type == 'corpo' and no.child[i].child[i].type != 'vazio'):
        aux = no.child[i].child[i+1]
        no.child[i] = no.child[i].child[i]
        no.child.insert(i+1, aux)
        podaCorpo(no)


def podaArvore(no):
    if(not no):
        return
    if(no.type == 'programa'):
        podaPrograma(no)
    elif(no.type == 'declaracao_variaveis'):
        podaDeclaracao_variaveis(no)
    elif(no.type == 'corpo'):
        podaCorpo(no)
    elif(no.type == 'atribuicao'):
       podaAtribuicao(no)
    elif(no.type == 'indice'):
       podaIndice(no)
    elif(no.type == 'acao'):
        podaAcao(no)
    elif(no.type == 'expressao_aditiva' or no.type == 'expressao_simples' or no.type == 'expressao_multiplicativa'):
        expressoes(no)
    elif(no.type == 'expressao'):
        podaExpressao(no,0)
    elif(no.type == 'lista_declaracoes'):
        podaListaDeclaracoes(no)
    elif(no.type == 'repita'):
        podaRepita(no)
    elif(no.type == 'parametro'):
        podaParametro(no)
    elif(no.type == 'lista_declaracoes'):
        listaDeclaracoes(no)

    for filho in no.child:    
        podaArvore(filho)

#########################################################teste

class elTab():
    def __init__(self, scopo, tipo, acao, valor, aux=[]):
        self.scopo = scopo
        self.tipo = tipo
        self.acao = acao
        self.valor = valor
        self.aux = aux

def printTabelaSimbolo(list):
    for l in list:
        print(l.scopo,l.tipo,l.acao,l.valor,l.aux)


def declaracaoVariaveis(no):
    vet = pegaVariavel(no)
    tipo = vet.pop(0)
    for v in vet:
        tabelaSimbolo.append(elTab(scopo[0], tipo, 'declaracao',str(v)))
    
def atribuicao(no):
    vet = pegaVariavel(no)
    tipo = vet.pop(0)
    aux = []
    for i in range(vet.__len__()):
        if(vet[i] == '+' or vet[i] == '-' or vet[i] == '/' or vet[i] == '*'):
            continue
        else:
            aux.append(vet[i])
    
    tabelaSimbolo.append(elTab(scopo[0], '', 'atribuicao', str(tipo), aux))


def chamadaFuncao(no):
    print(no)


def tabela(no):
    if(not no):
        return

    if(no.type == 'declaracao_funcao'):
        if(no.child.__len__() == 1):
            scopo.insert(0, no.child[0].value)
        else:
            scopo.insert(0, no.child[1].value)
    elif(no.type == 'declaracao_variaveis'):
        declaracaoVariaveis(no)
    elif(no.type == 'atribuicao'):
        atribuicao(no)
    elif(no.type == 'chamada_funcao'):
        chamadaFuncao(no)

    for filho in no.child:
        tabela(filho)



######################################################################################


def testaPrincipal(tabelaSimbolo):
    for obj in tabelaSimbolo:
        if(obj.scopo == 'principal'):
            return True
    return False



# def testaVariaveNaolUtilisada(tabelaSimbolo):
#     vetVariaveisDeclarada  = []

#     for obj in tabelaSimbolo:
#         if(obj.acao == 'declaracao'):
#             vetVariaveisDeclarada.append(obj)




# def msgWarning(tabelaSimbolo):
#     # if(not testaPrincipal(tabelaSimbolo)):
#     #     print('Erro nao possui principal')
#     printTabelaSimbolo(tabelaSimbolo)





tabelaSimbolo = []
scopo = []
scopo.append('global')

arq = open(sys.argv[1], 'r', encoding='utf-8')
data = arq.read()
arq.close()

result = parser.parse(data, tracking=True)

tabela(result)
# podaArvore(result)

# msgWarning(tabelaSimbolo)
# geraArvoreGraph(result, contemErros, True)
