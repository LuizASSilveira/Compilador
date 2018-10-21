from auxiliar import geraArvoreGraph, printArvore2
from lex import lexer
from Yacc import parser
import sys

def lexico(cod):
    lexer.input(cod)
    i = 0
    print('\n')
    while True:
        tok = lexer.token()
        if not tok:
            break
        print('( {}, {} )'.format(tok.type,tok.value)) #print(tok.type, tok.value, tok.lineno, tok.lexpos
        i += 1
    print('\n')

def sintatico(cod, bol):
    result = parser.parse(data)
    printArvore2(result)    
    if(bol):
        geraArvoreGraph(result)

arq = open(sys.argv[1],'r', encoding='utf-8')
data = arq.read()
arq.close()

try:
    if(sys.argv[2]):
        if(sys.argv[2] == '1'):
            lexico(data)
        elif(sys.argv[2] == '2'):
            sintatico(data,True)
except:
    print('error')
