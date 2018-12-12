import sys
from llvmlite import ir
from semantica import *

class Geracao():
    def __init__(self, modulo, no):
        self.modulo = modulo
        self.scopoGera = 'global'
        self.builder = None
        self.endBasicBlock = None
        self.entryBlock = None
        self.funcao = None
        self.varGlobal = {}
        self.varLocal = {}
        self.no = no
        self.leiaFlutuante = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), []), 'leiaF')
        self.gerarCodigo(self.no)

        # self.leiaInteiro = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), []), 'leia')
        # print(self.modulo)
        # print('\n')

    def gerarCodigo(self,no):
        if(no.child[0].type == 'declaracao_funcao'):
            self.declaracaoFuncao(no.child[0])
        else:   
            self.listaDeclaracao(no.child[0])
    
    def listaDeclaracao(self,no):
        if(len(no.child) == 1):
            if(no.child[0].type == 'declaracao_funcao'):
                self.declaracaoFuncao(no.child[0])
            elif(no.child[0].type == 'declaracao_variaveis'):
                self.declaracaoVariavel(no.child[0])
        else:
            self.listaDeclaracao(no.child[0])
            if(no.child[1].type == 'declaracao_funcao'):
                self.declaracaoFuncao(no.child[1])
            elif(no.child[1].type == 'declaracao_variaveis'):
                self.declaracaoVariavel(no.child[1])

    def declaracaoVariavel(self,no):
        if(len(no.child[1].child) > 0):
            nomeVariavel=no.child[1].type
            if(self.scopoGera == 'global'):
                if(no.child[0].type == 'inteiro'):
                    tipoA = ir.ArrayType(ir.IntType(64), int(no.child[1].child[0].type))
                    arrayA = ir.GlobalVariable(self.modulo, tipoA, name=nomeVariavel)
                    arrayA.align = 16
                else:
                    if(no.child[0].type == 'flutuante'):
                        tipoA = ir.ArrayType(ir.FloatType(), float(no.child[1].child[0].type))
                        arrayA = ir.GlobalVariable(
                        self.modulo, tipoA, name=nomeVariavel)
                        arrayA.align = 16
                self.varGlobal[nomeVariavel] = (arrayA)
            else:
                if(no.child[0].type == 'inteiro'):
                    var = self.builder.alloca(ir.IntType(32), name=nomeVariavel)
                else:
                    var = self.builder.alloca(ir.FloatType(), name=nomeVariavel)
                self.varLocal[self.scopoGera + '#' + nomeVariavel] = (var)
        else:
            if(self.scopoGera == 'global'):
                for i in range(1, len(no.child)):
                    nomeVariavel = no.child[i].type
                    if(no.child[0].type == 'inteiro'):
                        var = ir.GlobalVariable(self.modulo, ir.IntType(32), name=nomeVariavel)
                        var.initializer = ir.Constant(ir.IntType(32), 0)
                        var.linkage = 'common'
                        var.align = 4

                    else:
                        if(no.child[0].type == 'flutuante'):
                            var = ir.GlobalVariable(self.modulo, ir.FloatType(), name=nomeVariavel)
                            var.initializer = ir.Constant(ir.FloatType(), 0)
                            var.linkage = 'common'
                            var.align = 4
                    self.varGlobal[nomeVariavel] = (var)
            else:
                for i in range(1, len(no.child)):
                    nomeVariavel = no.child[i].type
                    if(no.child[0].type == 'inteiro'):
                        var = self.builder.alloca(ir.IntType(32), name=nomeVariavel)

                    else:
                        var = self.builder.alloca(
                            ir.FloatType(), name=nomeVariavel)
                    self.varLocal[self.scopoGera + '#' + nomeVariavel] = (var)

    def declaracaoFuncao(self,no):
        self.scopoGera = no.child[1].value
        parametros = []
        if(len(no.child) > 1):
            nomeF = no.child[1].value
            if(nomeF == 'principal'):
                nomeF = 'main'
            if(no.child[1].child[0].child[0].type == 'vazio'):  # função sem parametros
                if(no.child[0].value == 'inteiro'):
                    self.funcao = ir.Function(
                        self.modulo, ir.FunctionType(ir.IntType(32), ()), str(nomeF))
                else:
                    self.funcao = ir.Function(
                        self.modulo, ir.FunctionType(ir.FloatType(), ()), str(nomeF))
            else:
                par = []
                par2 = []
                for parans in no.child[1].child[0].child:  # pega Parametros
                    value = str(parans.child[0])
                    if(parans.type == 'flutuante'):
                        par.append(['flutuante', value])
                    else:
                        par.append(['inteiro', value])

                for p in par:
                    par2.append(self.tipo_parametros(p[1], p[0]))
                parametros = [par2[i][0][0] for i in range(0, len(par2))]

                if(no.child[0].value == 'inteiro'):
                    self.funcao = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), (parametros)), nomeF)
                else:
                    self.funcao = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), (parametros)), nomeF)

            self.entryBlock = self.funcao.append_basic_block(name="entry")
            self.endBasicBlock = self.funcao.append_basic_block('exit')
            self.builder = ir.IRBuilder(self.entryBlock)

            if(len(parametros)):
                for i, v in enumerate(par2):
                    self.funcao.args[i].name = v[0][1]
                    a = self.builder.alloca(v[0][0], name=v[0][1])
                    self.builder.store(self.funcao.args[i], a)
                    self.builder.load(a)
                    self.varLocal[self.scopoGera + '#' + v[0][1] ] = a
        
        if(no.child[1].child[1].type == 'corpo'):
            self.corpo(no.child[1].child[1])

    def corpo(self, no):
        for corpoFilho in no.child:
            if(corpoFilho.type == 'declaracao_variaveis'):
                self.declaracaoVariavel(corpoFilho)
            elif(corpoFilho.type == 'atribuicao'):
                self.atribuicao(corpoFilho)
            elif(corpoFilho.type == 'retorna'):
                self.retorna(corpoFilho)
            elif(corpoFilho.type == 'se'):
                self.se(corpoFilho)
            elif(corpoFilho.type == 'repita'):
                self.repita(corpoFilho)
            elif(corpoFilho.type == 'leia'):
                self.leia(corpoFilho)
            elif(corpoFilho.type == 'escreva'):
                self.escreva(corpoFilho)

    def repita(self,no):
        
        blocoRepita = self.builder.append_basic_block('repita')
        blocoFim = self.builder.append_basic_block('fim')
        
        self.builder.branch(blocoRepita)
        self.builder.position_at_end(blocoRepita)

        self.corpo(no.child[0])
        blocoRepita = self.builder.basic_block

        op = no.child[1].child[0].type
        val1 = no.child[1].child[0].child[0].type
        val2 = no.child[1].child[0].child[1].type

        val1 = self.defineOperandos(val1)
        val2 = self.defineOperandos(val2)

        print(val1,op, val2)

        if(op == '='):
            condicao = self.builder.icmp_signed('==', val1, val2, name='Igualdade')
        
        self.builder.cbranch(condicao, blocoRepita, blocoFim)
        self.builder.position_at_end(blocoFim)

    def ehNumero(self,valor):
        if('.' in valor):
            val = float(valor)
        else:
            try:
                val = int(valor)
            except:
                val = False
        return val

    def defineOperandos(self,val1,leia=False):
        
        if(type(val1) == int or type(val1) == float):

            if(type(val1) == float):
                val1 = ir.Constant(ir.FloatType(), val1)
            else:
                val1 = ir.Constant(ir.IntType(32), val1)
        
        else:
            aux = self.ehNumero(val1)
            tipe = type(aux)
            if(tipe != int and tipe != float and aux == False):
                val11 = self.qualScopo(val1)
                if(leia):
                    return val11
                val1 = self.builder.load(val11, self.scopoGera + '#' + val1)
            else:
                if(type(val1) == float):
                    val1 = ir.Constant(ir.FloatType(), val1)
                else:
                    val1 = ir.Constant(ir.IntType(32), val1)
        return val1

    def se(self,no):
        blocoEntao = self.funcao.append_basic_block(name='entao')
        if(len(no.child) == 3):
            blocoSenao = self.builder.append_basic_block('senao')
        blocoFim = self.funcao.append_basic_block(name='fim')

        if(no.child[0].child[0].type == 'expressao_simples'):
            noAux = no.child[0].child[0]
            op = noAux.child[0].type
            
            val1 = noAux.child[0].child[0].type
            val2 = noAux.child[0].child[1].type

            val1 = self.defineOperandos(val1)
            val2 = self.defineOperandos(val2)
            
            comparaSe = self.builder.icmp_signed(op, val1, val2, name="se_"+op)
            if(len(no.child) == 3):
                self.builder.cbranch(comparaSe, blocoEntao, blocoSenao)
            else:
                self.builder.cbranch(comparaSe, blocoEntao, blocoFim)	
            self.builder.position_at_end(blocoEntao)
            
            # self.atribuicao(no.child[1].child[0])
            self.corpo(no.child[1])
            self.builder.branch(blocoFim)

            if(len(no.child) == 3):
                self.builder.position_at_end(blocoSenao)
                self.corpo(no.child[2])
                self.builder.branch(blocoFim)
            
            self.builder.position_at_end(blocoFim)

    def retorna(self,no):
        if(no.child[0].type == 'var'):
            var2 = no.child[0].value
            var2 = self.qualScopo(var2)
            aux = self.builder.load(var2, self.scopoGera + '#' + no.child[0].value)

            retorna = self.builder.alloca(ir.IntType(32), name='retorna')
            retorna.align = 4
            
            self.builder.store(aux, retorna)
            self.builder.branch(self.endBasicBlock)
            self.builder.position_at_end(self.endBasicBlock)
            returnVal_temp = self.builder.load(retorna, name='ret_temp', align=4)
            self.builder.ret(returnVal_temp)

        elif(no.child[0].type == 'expressao_aditiva'):
            retorna = self.builder.alloca(ir.IntType(32), name='retorna')
            retorna.align = 4
           
            exp = self.expreAddAuxiliar(no.child[0], 'retorna')
            self.builder.store(exp, retorna)
            self.builder.branch(self.endBasicBlock)
            self.builder.position_at_end(self.endBasicBlock)
            returnVal_temp = self.builder.load(retorna, name='ret_temp', align=4)
            self.builder.ret(returnVal_temp)
        
        else:
            if('.' in no.child[0].type):
                retorna = self.builder.alloca(ir.FloatType(), name='retorna')
                retorna.align = 4
                num = ir.Constant(ir.FloatType(), float(no.child[0].type))
                self.builder.store(num, retorna)
                self.builder.branch(self.endBasicBlock)
                self.builder.position_at_end(self.endBasicBlock)
                returnVal_temp = self.builder.load(retorna, name='ret_temp', align=4)
                self.builder.ret(returnVal_temp)
            else:
                retorna = self.builder.alloca(ir.IntType(32), name='retorna')
                retorna.align = 4
                num = ir.Constant(ir.IntType(32), int(no.child[0].type))
                self.builder.store(num, retorna)
                self.builder.branch(self.endBasicBlock)
                self.builder.position_at_end(self.endBasicBlock)
                returnVal_temp = self.builder.load(retorna, name='ret_temp', align=4)
                self.builder.ret(returnVal_temp)

    def expreAddAuxiliar(self,no,var):
        pilha = []
        self.expressaoAditiva(no, pilha)
        p2 = []
        for p in pilha:
            if('.' in p):
                value = float(p)
                p2.append(ir.Constant(ir.FloatType(), value))
            else:
                try:
                    value = int(p)
                    p2.append(ir.Constant(ir.IntType(32), value))
                except:
                    if(p != '+' and p != '-' and p != '*'):
                        p2.append(self.qualScopo(p))
                    else:
                        p2.append(p)
        
        a = p2.pop(0)
        b = p2.pop(0)
        c = p2.pop(0)
        if(not 'Constant' in str(type(c))):
            c = self.builder.load(c)
            
        if(not 'Constant' in str(type(a))):
            a = self.builder.load(a)

        if(type(a) != type(b) and 'i32' in str(type(a))):
            a = self.builder.fptosi(a, ir.IntType(32))
            
        return self.calcula_expressao(a, b, c, var)
        
    def atribuicao(self,no):
        var = no.child[0].value
        if(no.child[1].type == 'numero'):
            
            valor = self.qualScopo(var)
            
            value = no.child[1].value
            value = self.defineOperandos(value)

            if( 'i32' in str(valor.type) and (not 'i32' in str(value.type))):
                if(not 'i32' in str(var.type)):
                    value = self.builder.sitofp(value, ir.FloatType())
                else:
                    value = self.builder.fptosi(value, ir.IntType(32))
            
            
            self.builder.store(value, valor)
       
        
        elif(no.child[1].type == 'var'):
            var1 = no.child[0].value
            var1 = self.qualScopo(var1)

            var2 = no.child[1].value
            var2 = self.qualScopo(var2)            
            aux = self.builder.load(var2, self.scopoGera +'#'+ no.child[1].value)
            
            if(var1.type == var2.type):
                self.builder.store(aux, var1)
            else: #fazer coercao
                pass
        elif(no.child[1].type == 'expressao_aditiva'):
            exp = self.expreAddAuxiliar(no.child[1], var)
            var = self.qualScopo(var)

            if('i32' in str(var.type)):
                exp = self.builder.fptosi(exp, ir.IntType(32))
            
            
            self.builder.store(exp, var)
        
        elif(no.child[1].type == 'chamada_funcao'):
            nomeVar = no.child[0].value
            var = self.qualScopo(nomeVar)
            
            nomeFunc = no.child[1].value
            func = self.modulo.get_global(nomeFunc)

            parametros = []
            
            for arg in no.child[1].child[0].child:
                parametros.append(self.defineOperandos(arg.type))

            chamadaFun = self.builder.call(func, parametros, name= 'chamadaFun' )
            
            
            if(var.type != chamadaFun):
                if('i32' in str(var.type)):
                    chamadaFun = self.builder.fptosi(chamadaFun, ir.IntType(32))
                else:
                    chamadaFun = self.builder.sitofp(chamadaFun, ir.FloatType())

            self.builder.store(chamadaFun, var)

    def calcula_expressao(self, expEsquerda, operador, expDireita, var):
        
        if(operador == "+"):
            return self.builder.add(expEsquerda, expDireita, name="add_"+var, flags=())
        elif(operador == "-"):
            return self.builder.sub(expEsquerda, expDireita, name="sub_"+var, flags=())
        elif(operador == "*"):
            return self.builder.mul(expEsquerda, expDireita, name="mul_"+var, flags=())
        else:
            return self.builder.mul(expEsquerda, expDireita, name="div_"+var, flags=())
            
    def expressaoAditiva(self,no,pilha):
        if(no.child[0].child[0].type != 'expressao_aditiva'):
            pilha.append(no.child[0].child[0].type)
            pilha.append(no.child[0].type)
            pilha.append(no.child[0].child[1].type)
        else:
            self.expressaoAditiva(no.child[0].child[0], pilha)
            pilha.append(no.child[0].type)
            pilha.append(no.child[0].child[1].type)

    def qualScopo(self,var):
        scoVar = self.scopoGera + '#' + var
        if(scoVar in self.varLocal):  # verifica em qual escopo
            valor = self.varLocal[scoVar]
        else:
            valor = self.varGlobal[var]
        return valor

    def tipo_parametros(self,valorParam, parametros):
        tipo = []
        if(parametros == "inteiro"):
            conv = ir.IntType(32)
        else:
            conv = ir.FloatType()

        tipo.append((conv, valorParam))
        return tipo

    def leia(self, no):
        
        var = self.defineOperandos(no.child[0].type,True)

        valor = self.builder.call(self.leiaFlutuante, [])
        #sitofp

        if('i32' in str(var.type)):
            valor = self.builder.fptosi(valor, ir.IntType(32))        
                
        self.builder.store(valor, var)
            
    def escreva(self,no):

        if(len(no.child) == 1):
            var = self.defineOperandos(no.child[0].type)
            if('i32' in  str(var.type)):
                escrevaInt = ir.Function(self.modulo, ir.FunctionType(ir.IntType(32), [ir.IntType(32)]), 'escrevaInteiro')
                self.builder.call(escrevaInt, [var])
            else:
                escrevaFlut = ir.Function(self.modulo, ir.FunctionType(ir.FloatType(), [ir.FloatType()]), 'escrevaFlutuante')
                self.builder.call(escrevaFlut, [var])	
            
def geracaoCodico(data):
    no = semanticaGeracodigo(data, False)
    # no = semanticaGeracodigo(data)
    ger = Geracao(ir.Module('LUIZ2'),no)
    print(str(ger.modulo))
    arquivo = open('gera.ll', 'w')
    arquivo.write(str(ger.modulo))
    arquivo.close()
    # printTabelaSimbolo(tabelaSimbolo)


