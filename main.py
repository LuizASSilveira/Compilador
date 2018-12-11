from auxiliar import geraArvoreGraph, Tree
from lex import lexer
from Yacc import parser,contemErros
import sys
from semantica import analiseSemantica
from geraCodigoV2 import geracaoCodico

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
    analiseSemantica(data)
      
def codigo(data):
    geracaoCodico(data)

arq = open(sys.argv[1],'r', encoding='utf-8')
data = arq.read()
arq.close()

try:
    if(sys.argv.__len__() <= 2):
        lexico(data)
        sintatico(data)
        analiseSemantica(data)
        codigo(data)
    else:
        if(sys.argv[1]):
            if(sys.argv[2] == '--lexico'):
                lexico(data)
            elif(sys.argv[2] == '--sintatico'):
                sintatico(data)
            elif(sys.argv[2] == '--semantico'):
                semantico(data)
            elif(sys.argv[2] == '--geracaoCodigo'):
                codigo(data)
            else:
                print(
                    'Comando esperados:',
                    '\t--lexico',
                    '\t--sintatico',
                    '\t--semantico',
                )

except IndexError as er:
    print('error = ', er)
