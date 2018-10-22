from auxiliar import geraArvoreGraph as printArvore
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
    printArvore(result, bol)

arq = open(sys.argv[1],'r', encoding='utf-8')
data = arq.read()
arq.close()

try:
    if(sys.argv.__len__() <= 2):
        lexico(data)
        sintatico(data, True)
    else:
        if(sys.argv[1]):
            if(sys.argv[1] == '1'):
                lexico(data)
            elif(sys.argv[2] == '2'):
                sintatico(data,True)

except IndexError as er:
    print('error = ', er)
