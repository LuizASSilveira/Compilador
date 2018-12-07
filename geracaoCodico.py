#!/usr/bin/env python
# -*- coding: utf-8 -*

import sys

from llvmlite import ir

from semantica import *


def geraDeclaracaoVariaveis(node):
    if(node.child[1].child):
        nomeVariavel = node.child[1].type
        if(scopoGera[0] == 'global'):
            if(node.child[0].type == 'inteiro'):
                tipoA = ir.ArrayType(ir.IntType(64),int(node.child[1].child[0].type))
                arrayA = ir.GlobalVariable(modulo, tipoA, nomeVariavel)
                arrayA.align = 16
            else:
                if(node.child[0].type == 'flutuante'):
                    tipoA = ir.ArrayType(ir.FloatType(), node.child[1].child[0].type)
                    arrayA = ir.GlobalVariable(modulo, tipoA, nomeVariavel)
                    arrayA.align = 16
        # else:
        #     if(node.child[0].type == 'inteiro'):
        #         builder.alloca(ir.IntType(32), nomeVariavel)
            
        #     if(node.child[0].type == 'flutuante'):
        #         builder.alloca(ir.FloatType(), nomeVariavel)
            
    else:
        if(scopoGera[0] == 'global'):
            for i in range(1,len(node.child)):

                nomeVariavel = node.child[i].type
                if(node.child[0].type == 'inteiro'):
                    var = ir.GlobalVariable(modulo, ir.IntType(32), nomeVariavel)
                    var.initializer = ir.Constant(ir.IntType(32), 0)
                    var.linkage = 'common'
                    var.align = 4
            
                else:
                    if(node.child[0].type == 'flutuante'):
                        var = ir.GlobalVariable(modulo, ir.FloatType(), nomeVariavel)
                        var.initializer = ir.Constant(ir.FloatType(), 0)
                        var.linkage = 'common'
                        var.align = 4


def geraDeclaracaoFuncao(no):
    nomeF = no.type
    if(no.type == 'principal'):
        nomeF = 'main'

    if(len(no.child) > 1):
        if(no.child[1].child[0].child[0].type == 'vazio'): #função sem parametros
            if(no.child[0].value == 'inteiro'):
                funcao = ir.Function(modulo, ir.FunctionType(ir.IntType(32), ()), nomeF)
            else:
                funcao = ir.Function(modulo, ir.FunctionType(ir.FloatType(), ()), nomeF)
        else:

            parametros = []
            for parans in no.child[1].child[0].child: #pega Parametros
                if(parans.type == 'flutuante'):
                    parametros.append((ir.FloatType() , parans.child[0].type))
                else:
                    parametros.append((ir.IntType(32), parans.child[0].type))

            print(parametros)

            # if(no.child[0].value == 'inteiro'):
            #     funcao = ir.Function(modulo, ir.FunctionType(ir.IntType(32), (parametros)), nomeF)
            # else:
            #     funcao = ir.Function(modulo, ir.FunctionType(ir.FloatType(), (parametros)), nomeF)

def geraCodigo(no):

    if(not no):
        return

    if(no.type == 'declaracao_funcao'):
        if(no.child.__len__() == 1):
            scopo.insert(0, no.child[0].value)
        
          
    if(no.type == 'declaracao_variaveis'):
        geraDeclaracaoVariaveis(no)
    elif(no.type == 'declaracao_funcao'):
        geraDeclaracaoFuncao(no)


    for filho in no.child:
        geraCodigo(filho)

#arquivo
arq = open(sys.argv[1], 'r', encoding='utf-8')
data = arq.read()
arq.close()

scopoGera = []
scopoGera.append('global')

modulo = ir.Module('Meu_modulo')

no = semanticaGeracodigo(data, False)
# no = semanticaGeracodigo(data)
# printTabelaSimbolo(tabelaSimbolo)


geraCodigo(no)
print(modulo)
