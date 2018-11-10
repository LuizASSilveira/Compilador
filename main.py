from auxiliar import geraArvoreGraph, Tree
from lex import lexer
from Yacc import parser,contemErros
import sys
from semantica import podaArvore

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

def sintatico(cod, bol = True):
    result = parser.parse(data, tracking=True)
    geraArvoreGraph(result, contemErros ,bol)

def semantico(data):
    
    result = parser.parse(data, tracking=True)
    geraArvoreGraph(result, contemErros,True)
    
    arvore = Tree('programa')
    podaArvore(result)
    
arq = open(sys.argv[1],'r', encoding='utf-8')
data = arq.read()
arq.close()

try:
    if(sys.argv.__len__() <= 2):
        lexico(data)
        sintatico(data)
    else:
        if(sys.argv[1]):
            if(sys.argv[1] == '1'):
                lexico(data)
            elif(sys.argv[2] == '2'):
                sintatico(data)
            elif(sys.argv[2] == '3'):
                semantico(data)

except IndexError as er:
    print('error = ', er)
