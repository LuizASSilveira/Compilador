from auxiliar import visaoSemantica, Tree
from lex import lexer
from Yacc import parser, contemErros
import sys
from collections import defaultdict
import colorama

errosSemanticos = []
warningSemantico = []

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

    if(no.child[1].child[0].child.__len__() != 0 and no.child[1].child[0].type != 'lista_variaveis'):
        
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
    
    if(no.child[0].type == 'escreva' or no.child[0].type == 'leia'):
        var = encontraFolha(no.child[0])
        no.child[0].child[0] = Tree(var.value)

    elif(no.child[0].type != 'retorna'):
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

def podaListaArgumentos(no):
    var = pegaVariavel(no)
    if(len(var)):
        no.child = []
        for v in var:
            no.child.insert(0,Tree(str(v)))

def podaCabecalho(no):
    
    if(len(no.child[0].child) != 1): 
        variavel = []
        vet = []
        noAux = no.child[0]

        while(True):
            if(noAux.value):
                variavel.append(noAux.value)
            
            for son in noAux.child:
                vet.append(son)
            
            if(len(vet) == 0):
                break
            noAux = vet.pop(0)

        no.child[0].child = []

        tipo = []
        num = []

        for v in variavel:    
            if(v != 'inteiro' and v != 'flutuante'):
                num.insert(0,v)     
                # no.child[0].child.insert(0,Tree(v))
            else:
                tipo.insert(0,v)
        
        for i in range(len(tipo)):
            no.child[0].child.insert(0, Tree(tipo[i],[Tree(num[i])],))

def podaRetorna(no):
    var = encontraFolha(no)

    if(var.type == 'numero'):
        no.child = []
        no.child.append(Tree(str(var.value)))
    else:
        no.child = []
        no.child.append(var)

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
    elif(no.type == 'lista_argumentos'):
        podaListaArgumentos(no)
    elif(no.type == 'cabecalho'):
        podaCabecalho(no)
    elif(no.type == 'retorna'):
        podaRetorna(no)
    
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
        print(l.scopo, l.tipo, l.acao, l.valor, l.aux)

def declaracaoVariaveis(no):

    tipo = no.child[0].type   
        
    if(len(no.child[1].child) == 0):
        var = []
        for v in no.child:
            var.append(v.type)
        var.pop(0)
        tabelaSimbolo.append(elTab(scopo[0], tipo, 'declaracaoVariaveis',var))
        
    else:
        var = []
        
        for v in no.child[1].child:
            var.append(v.type)

        if(len (no.child[1].child) == 0):
            tabelaSimbolo.append(elTab(scopo[0], tipo, 'declaracaoVariaveis',var))#modificado
        else:
            tabelaSimbolo.append(
                elTab(scopo[0], tipo, 'declaracaoVariaveis', [no.child[1].type], var))  # modificado

def retornaNoType(no):
    variavel = []
    vet = []
    noAux = no

    while(True):
        if(noAux.type != 'expressao_aditiva' and noAux.type != 'expressao_multiplicativa'):
            variavel.append(noAux.type)
        for son in noAux.child:
            vet.append(son)
        if(len(vet) == 0):
            break
        noAux = vet.pop(0)
    variavel.__reversed__()
    return variavel

def atribuicao(no):
    if(no.child[0].value and no.child[1].value):
        tabelaSimbolo.append(elTab(scopo[0], '', 'atribuicao', no.child[0].value, [no.child[1].value]))
    elif(no.child[1].type == 'expressao_aditiva' or no.child[1].type == 'expressao_multiplicativa'):       
        oper = retornaNoType(no.child[1])
        tabelaSimbolo.append(elTab(scopo[0], '', 'atribuicao', no.child[0].value, oper))
    
def expressaoSimples(no):
    oper = retornaNoType(no.child[0])
    tabelaSimbolo.append(elTab(scopo[0], '', 'expressaoSimples', '', oper))

def chamadaFuncao(no):
    listArg = []
    for a in no.child[0].child:
        listArg.append(a.type)
    tabelaSimbolo.append(elTab(scopo[0], '', 'chamadaFuncao', no.value, listArg))

def cabecalho(no):
    parametros = []
    cabDelaracao = []
    for par in no.child[0].child:
        if(par.type != 'vazio'):
            parametros.append([par.type,par.child[0].type])
            cabDelaracao.append([par.type, par.child[0].type])
        else:
            parametros.append(par.type)
    tabelaSimbolo.append(elTab(scopo[0], '', 'cabecalho', scopo[0], parametros))

    for cab in cabDelaracao:
        tabelaSimbolo.append(elTab(scopo[0], cab[0], 'declaracaoVariaveis', [cab[1]]))

def retorna(no):
    if(not len(no.child[0].child)):
        if(len(no.child[0].value) > 0):
            tabelaSimbolo.append(elTab(scopo[0], '', 'retorna', '', [no.child[0].value]))
        else:
            tabelaSimbolo.append(elTab(scopo[0], '', 'retorna', '', [no.child[0].type]))
    else:
        vet = retornaNoType(no.child[0])
        tabelaSimbolo.append(elTab(scopo[0], '', 'retorna', '', vet))

def escreva(no):
    listAux = retornaNoType(no.child[0])
    listRemove = ['+','/','*','-']

    for r in listRemove:
        if(r in listAux):
            listAux.remove(r)

    tabelaSimbolo.append(elTab(scopo[0], '', 'escreva', '', listAux))
    
def leia(no):
    if(len(no.child) > 0):
        tabelaSimbolo.append(elTab(scopo[0], '', 'leia', '', [no.child[0].value]))

def tabela(no):
    if(not no):
        return
    
    if(no.type == 'declaracao_funcao'):
        if(no.child.__len__() == 1):
            scopo.insert(0, no.child[0].value)
            tabelaSimbolo.append(
                elTab(scopo[0], 'vazio', 'declaracao_funcao', no.child[0].value))
        else:
            scopo.insert(0, no.child[1].value)
            tabelaSimbolo.append(elTab(scopo[0], no.child[0].value, 'declaracao_funcao', no.child[1].value))

    elif(no.type == "declaracao_variaveis"):
        declaracaoVariaveis(no)
    elif(no.type == 'atribuicao'):
        atribuicao(no)
    elif(no.type == 'expressao_simples'):
        expressaoSimples(no)
    elif(no.type == 'chamada_funcao'):
        chamadaFuncao(no)
    elif(no.type == 'cabecalho'):
        cabecalho(no)
    elif(no.type == 'retorna'):
        retorna(no)
    elif(no.type == 'escreva'):
        escreva(no)
    elif(no.type == 'leia'):
        leia(no)

    for filho in no.child:
        tabela(filho)

######################################################################################

def testNumero(val):
    
    if('.' in str(val)):
        return False
    else:
        try:
            int(val)
            return False
        except:
            return val

def notSimbolo(var):
    if(var == '/' or var == '*' or var == '-' or var == '+' or var == '>' or var == '=' or var == '<' or var == '<=' or var == '>=' or var =='inteiro' or var == 'flutuante'):
        return False
    else:
        return True

def testaPrincipal(tabelaSimbolo):
    for obj in tabelaSimbolo:
        if(obj.scopo == 'principal'):
            testPrincipalRetorno(tabelaSimbolo)  
            return     
    errosSemanticos.append('Erro: Função principal não declarada')

def testIndiceVetor(tabelaSimbolo):
    pass
    for tb in tabelaSimbolo:
        if(tb.acao == 'declaracaoVariaveis'):
            for v in tb.aux:
                if('.' in v):
                    errosSemanticos.append('Erro: índice de array '+ str(v) + ' não inteiro')
                    return
    return

def testPrincipalRetorno(tabelaSimbolo):
    for ret in tabelaSimbolo:
        if(ret.scopo == 'principal' and ret.acao == 'retorna' and ret.aux.__len__() > 0):
        # if(ret.scopo == 'principal' and ret.acao == 'retorna'):
            return
    errosSemanticos.append('Erro: Função principal deveria retornar inteiro')  

def testFuncaoChamdaeNaoDeclarada(tabelaSimbolo):
    declarado = []
    funcChamado = []

    for aux in tabelaSimbolo:
        if(aux.acao == 'cabecalho' and aux.valor != 'principal'):
            declarado.append(aux.valor)
        elif(aux.acao == 'chamadaFuncao'):
            funcChamado.append(aux.valor)

    if(declarado != funcChamado):
        declarado = set(declarado)
        funcChamado = set(funcChamado)
        naoD = funcChamado - declarado

        for n in naoD:
            if(n != 'principal'):
                errosSemanticos.append('Erro: Chamada a função "'+ n +'" que não foi declarada')

def testParamError(tabelaSimbolo):
    declarado = {}
    funcChamado = {}

    for aux in tabelaSimbolo:
        if(aux.acao == 'cabecalho' and aux.valor != 'principal'):
            declarado[aux.valor] = [aux.acao , len(aux.aux)]
        elif(aux.acao == 'chamadaFuncao'):            
            funcChamado[aux.valor] = [aux.acao , len(aux.aux)]

    for cabTam in declarado.keys():        
        try:
            funcChamado[cabTam][1]
            declarado[cabTam][1]
        except:
            return
                
        if(declarado[cabTam][1] != funcChamado[cabTam][1]):
           errosSemanticos.append('Erro: Chamada de função "' + cabTam + '" com número incorreto de argumentos')
                
def descobreTipo(tab,tabelaSimbolo):
    resp = ''
    for aux in tabelaSimbolo:
        if(aux.acao == 'declaracaoVariaveis' and (aux.scopo == 'global' or aux.scopo == tab.scopo)):#verifica se ele nao achou ele mesmo
            for var in aux.valor:
                if(tab.valor == var):
                    resp = aux.tipo
        elif(aux.acao == 'declaracao_funcao' and tab.valor == aux.valor): #decobre tipo funcao
            resp = aux.tipo
            return resp        
    return resp

def descobreTipo2(tab,tabelaSimbolo):
    resp = ''
    fun = False
    for aux in tabelaSimbolo:
        if(aux.acao == 'declaracaoVariaveis'):
            for v in aux.valor:
                if(v == tab):
                    resp = aux.tipo
            
        elif(aux.valor == tab and aux.acao == 'declaracao_funcao'):
            resp = aux.tipo
            fun = True
            return resp, fun

    return resp, fun

def testAtribuicaoIncorreta(tabelaSimbolo):
    atr = []

    for aux in tabelaSimbolo:
        if(aux.acao == 'atribuicao'):
            atr.append(aux)
    
    for a in atr:
        tipo = descobreTipo(a, tabelaSimbolo)     
        
        if(tipo == '' and type(tipo) == 'str'):
            errosSemanticos.append('Erro2: Variável ' + a + ' não declarada')
            return

        for aux in a.aux:
            if(aux != '+' and aux != '-' and aux != '/' and aux != '*'):   
                if('.' in str(aux)):
                    if(tipo != 'flutuante'):
                        warningSemantico.append('Aviso: Coerção implícita do valor atribuído para"' + str(a.valor) + '"')
                        return
                else:
                    try:
                        tipo2 = (int(aux))
                        if(tipo != 'inteiro'):
                            warningSemantico.append('Aviso: Coerção implícita do valor atribuído para "' + str(a.valor) + '"')
                            return

                    except:
                        tipo2,fun = descobreTipo2(aux, tabelaSimbolo)
                        # print('lllluizzzz', tipo2, aux)
                        if(tipo2 == ''):
                            errosSemanticos.append('Erro3: Variável "' + aux + '" não declarada')
                            return
                        elif(tipo != tipo2 ):
                            if(fun):
                                warningSemantico.append('Aviso: Coerção implícita do valor retornado por "' + aux + '"')
                                # warningSemantico.appendnt('Aviso: Atribuição de tipos distintos "', a.valor ,'"', tipo ,' e "', aux ,'" ',tipo2,'}')
                            else:
                                warningSemantico.append('Aviso: Coerção implícita do valor "' + aux + '"')
                                # warningSemantico.appendnt('Aviso: Atribuição de tipos distintos "', a.valor ,'"', tipo ,' e "', aux ,'" ',tipo2,'}') 

def variavelJaDeclarada(tabelaSimbolo):
    listDeclara = []
    for aux in tabelaSimbolo:
        if(aux.acao == 'declaracaoVariaveis'):
            var = str(aux.scopo) + str(aux.valor[0])
            if(var in listDeclara):
                warningSemantico.append('Aviso: Variável "' +aux.valor[0] + '" já declarada anteriormente')
            else:
                listDeclara.append(var)

def variavelNaoUtilizada(tabelaSimbolo):
    listIDeclarada = []
    listUtilisada = []

    for tb in tabelaSimbolo:
        if(tb.acao == 'declaracaoVariaveis'):
            for v in tb.valor:
                listIDeclarada.append(str(v))
        else:
            # if(tb.valor != '' and tb.acao != 'declaracao_funcao' and tb.acao != 'cabecalho' and tb.acao != 'atribuicao'):
            if(tb.valor != '' and tb.acao != 'declaracao_funcao' and tb.acao != 'cabecalho'):
                listUtilisada.append(tb.valor[0])
            
            if(tb.aux.__len__() > 0 and tb.aux[0] != 'vazio'):
                if(tb.acao != 'cabecalho'):
                    for a in tb.aux:
                        if(notSimbolo(a) and a != 'inteiro' and a != 'flutuante'):
                            listUtilisada.append(a)
                else:
                    for a in tb.aux[0]:
                        if(notSimbolo(a) and a != 'inteiro' and a != 'flutuante'):
                            listUtilisada.append(a)

    listIDeclarada = set(listIDeclarada)
    listUtilisada = set(listUtilisada)
    naoUti = listIDeclarada - listUtilisada
    
    cont = 0 
    if(len(naoUti) > 0):
        for n in naoUti:
            warningSemantico.append('Aviso: Variável "' + n + '" declarada e não utilizada')
            cont += 1

    if(cont == 0):
        return True
    else:
        return False

def variavelDeclaradaNaoInicialisada(tabelaSimbolo): 
    if(variavelNaoUtilizada(tabelaSimbolo)):
        for s in scopo:
            if(s == 'global'):
                continue
   
            listIDeclarada = []
            listAtri =  []
            listParam = []
            listAtrGlobal = []
            
            for tb in tabelaSimbolo:
                if(tb.acao == 'atribuicao' and (tb.scopo == 'global' or tb.scopo == s)):
                    listAtri.append(str(tb.valor[0]))
                    
                elif(tb.acao == 'declaracaoVariaveis' and (tb.scopo == 'global' or tb.scopo == s)):
                    if(tb.scopo == 'global'):
                        listAtrGlobal.append(str(tb.valor[0]))
                    listIDeclarada.append(str(tb.valor[0]))
                    
                elif(tb.acao == 'leia' and (tb.scopo == 'global' or tb.scopo == s)):
                    listAtri.append(str(tb.aux[0]))
                
                elif(tb.acao == 'cabecalho' and tb.scopo == s):
                    if(tb.aux[0] != 'vazio'):
                        for l in tb.aux:
                            # print(l)
                            if(type(l) == type(list('a'))):
                                listParam.insert(0,l[1])
                            else:
                                listParam.insert(0,l)
            
            listIDeclarada = set(listIDeclarada)
            listAtri = set(listAtri)
            # print('+++++',listParam)
            listParam = set(listParam)
            listAtrGlobal = set(listAtrGlobal)

            sob = (listIDeclarada - listAtri) - listParam            
            sob = sob - listAtrGlobal

            # print(sob)
            for s in sob:
                warningSemantico.append('Aviso: Variável "' + s + '" declarada e não inicializada')

def variavelNaoDeclarada(tabelaSimbolo): #nao declarada e utilisada
    funcDeclarada = []
    varDeclarada = defaultdict(list)
    varUtilisada = defaultdict(list)

    for aux in tabelaSimbolo:
        for sco in scopo:
            if(aux.acao == 'declaracaoVariaveis' and aux.scopo == sco):
                varDeclarada[sco].append(aux.valor)

            if(aux.acao == 'cabecalho' and (aux.valor != 'principal') and (not aux.valor in funcDeclarada)):
                funcDeclarada.append(aux.valor)
            
            if(len(aux.aux) and aux.aux[0] != 'vazio' and aux.scopo == sco and aux.acao != 'cabecalho'):
                varUtilisada[sco].append(aux.aux)

    varDeclarada2 = {}
    varUtilisada2 = {}

    for x in varDeclarada.keys():
        a1 = varDeclarada[x]
        saida = []
        for aux1 in a1:
            for aux2 in aux1:
                if(testNumero(aux2) and notSimbolo(aux2)):
                    saida.append(aux2)
        varDeclarada2[x] = saida

    for x in varUtilisada.keys():
        a1 = varUtilisada[x]
        saida = []
        for aux1 in a1:
            for aux2 in aux1:
                if(testNumero(aux2) and notSimbolo(aux2)):
                    saida.append(aux2)
        varUtilisada2[x] = saida
    
    # for sco in scopo:


    # for sco in scopo:
    #     for uti in varUtilisada[sco]:
    #         if(testNumero(uti[0]) and notSimbolo(uti[0])):
    #             if(((uti[0] != 'inteiro' and uti[0] != 'flutante') and  (not uti in varDeclarada[sco]) and (not uti in varDeclarada['global'])) and (not uti[0] in funcDeclarada)):
    #                 errosSemanticos.append('Erro: Variável "' + str(uti[0]) + '" não declarada')

def chamadaPrincipalNaoPermitida(tabelaSimbolo):
    for aux in tabelaSimbolo:
        if(aux.scopo != 'principal' and aux.acao == 'chamadaFuncao' and aux.valor == 'principal'):
            errosSemanticos.append('Erro: Chamada para a função principal não permitida')

def funcTipoRetornoErrado(tabelaSimbolo):
    for tb in tabelaSimbolo:
        if(tb.acao == 'declaracao_funcao' and tb.valor != 'principal'):
            for tb2 in tabelaSimbolo:
                if(notSimbolo(tb2) and tb2.acao == 'retorna' and tb2.scopo == tb.scopo and tb.scopo != 'principal'):
                    tipos = []
                    tipo = tb.tipo
                    for aux in tb2.aux:
                        if('.' in aux):
                            tipos.append('flutuante')
                        else:
                            try:
                                int(aux)
                                tipos.append('inteiro')
                            except:
                                a,b = descobreTipo2(aux, tabelaSimbolo)
                                tipos.append(a)

                    tipo = set([tipo])
                    tipos = set(tipos)
                    dif = tipos - tipo
                    dif = list(dif)
                    if('' in dif ):
                        dif.remove('')
                    if(len(dif)):
                        if(dif[0] == 'flutuante'):
                            errosSemanticos.append("Erro: Função '" + tb.valor +"' do tipo '" + tb.tipo + "' retornando '" + dif[0]+ "'")
                        else:
                            warningSemantico.append("Aviso: Função '" + tb.valor +"' do tipo '" + tb.tipo + "' retornando '" + dif[0]+ "'")

def chamadaRecursivaPrincipal(tabelaSimbolo):
    for aux in tabelaSimbolo:
        if(aux.acao =='chamadaFuncao' and aux.valor == 'principal' and aux.scopo == 'principal'):
            warningSemantico.append('Aviso: Chamada recursiva para principal')

def funcDeclaradaNaoUtilisada(tabelaSimbolo):
    funcChamada = []
    funcDeclarada = []

    for aux in tabelaSimbolo:
        if(aux.valor != 'principal'):
            if(aux.acao == 'chamadaFuncao'):
                funcChamada.append(aux.valor)
            elif(aux.acao == 'declaracao_funcao'):
                funcDeclarada.append(aux.valor)
    
    funcChamada = set(funcChamada)
    funcDeclarada = set(funcDeclarada)
    resp = funcDeclarada - funcChamada

    if(len(resp) != 0):
        resp = list(resp)
        for r in resp:
            warningSemantico.append('Aviso: Função "'+ r + '" declarada, mas não utilizada')

def msgWarning(tabelaSimbolo):
    variavelNaoDeclarada(tabelaSimbolo)
    testaPrincipal(tabelaSimbolo)
    testIndiceVetor(tabelaSimbolo)     
    testFuncaoChamdaeNaoDeclarada(tabelaSimbolo)
    testParamError(tabelaSimbolo)
    testAtribuicaoIncorreta(tabelaSimbolo)
    variavelJaDeclarada(tabelaSimbolo)
    variavelDeclaradaNaoInicialisada(tabelaSimbolo)
    chamadaPrincipalNaoPermitida(tabelaSimbolo)
    funcTipoRetornoErrado(tabelaSimbolo)
    chamadaRecursivaPrincipal(tabelaSimbolo)
    funcDeclaradaNaoUtilisada(tabelaSimbolo)

def poda2(no):
    
    if(not no):
        return

    if(no.type == 'corpo'):
        for i in range(len(no.child)):
            no.child[i] = no.child[i].child[0]
    
    for filho in no.child:
        poda2(filho)

tabelaSimbolo = []
scopo = []
scopo.append('global')

def analiseSemantica(data):
    result = parser.parse(data, tracking=True)
   
    global errosSemanticos, warningSemantico
    # visaoSemantica(result)
    podaArvore(result)
    tabela(result)
    

    # printTabelaSimbolo(tabelaSimbolo)
    if(len(tabelaSimbolo) != 0):
        msgWarning(tabelaSimbolo)

        # poda2(result)
        colorama.init()
        print('\n')
        if(len(errosSemanticos) > 0):  
            errosSemanticos = list(set(errosSemanticos))    
            for er in errosSemanticos:        
                print(colorama.Fore.LIGHTYELLOW_EX + er)
        # else:
        #     visaoSemantica(result)

        aletSemanticos = list(set(warningSemantico))
        for war in aletSemanticos:
            print(colorama.Fore.LIGHTYELLOW_EX + war)

        print('\n')

def semanticaGeracodigo(data,pr = True):
    result = parser.parse(data, tracking=True)

    global errosSemanticos, warningSemantico
    # visaoSemantica(result)
    podaArvore(result)
    tabela(result)

    # printTabelaSimbolo(tabelaSimbolo)
    if(len(tabelaSimbolo) != 0):
        msgWarning(tabelaSimbolo)

        poda2(result)
        colorama.init()
        print('\n')
        if(len(errosSemanticos) > 0):

            errosSemanticos = list(set(errosSemanticos))
            for er in errosSemanticos:
                print(colorama.Fore.LIGHTYELLOW_EX + er)
        else:
            if(pr):
                visaoSemantica(result)

        aletSemanticos = list(set(warningSemantico))
        for war in aletSemanticos:
            print(colorama.Fore.LIGHTYELLOW_EX + war)

        print('\n')
    return result