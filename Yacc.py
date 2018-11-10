# Yacc example
import ply.yacc as yacc
from lex import tokens
from auxiliar import Tree
import sys
import colorama

contemErros = False
linhasErros = []

precedence = (
    ('left', 'IGUALDADE', 'MAIOR_IGUAL', 'MENOR_IGUAL', 'MAIOR', 'MENOR', 'ATRIBUICAO'),
    ('left', 'SOMA', 'SUBTRACAO'),
    ('left', 'E_LOGICO','OU_LOGICO'),
    ('left', 'MULTIPLICACAO', 'DIVISAO'),
    ('left', 'NEGACAO'),
)

def p_programa(p):
    '''
    programa :  lista_declaracoes
    '''
    p[0] = Tree('programa', [p[1]])

def p_lista_declaracoes(p):
    '''
    lista_declaracoes :  declaracao
                        | lista_declaracoes declaracao
    '''
    if len(p) == 3:
        p[0] = Tree('lista_declaracoes', [p[1], p[2]])
    elif len(p) == 2:
        p[0] = Tree('lista_declaracoes', [p[1]])

def p_declaracao(p):
    '''
        declaracao : declaracao_variaveis
                | inicializacao_variaveis
                | declaracao_funcao
    '''
    p[0] = Tree('declaracao', [p[1]])

def p_declaracao_variaveis(p):
    '''
    declaracao_variaveis : tipo DOIS_PONTOS lista_variaveis
    '''
    p[0] = Tree('declaracao_variaveis', [p[1], p[3]])

def p_inicializacao_variaveis(p):
    '''
    inicializacao_variaveis : atribuicao
    '''
    p[0] = Tree('inicializacao_variaveis', [p[1]])

def p_lista_variaveis( p):
    '''
    lista_variaveis : lista_variaveis VIRGULA var
                    | var
    '''
    if len(p) == 4:
        p[0] = Tree('lista_variaveis', [p[1], p[3]])
    elif len(p) == 2:
        p[0] = Tree('lista_variaveis', [p[1]])

def p_var(p):
    '''
    var : ID
        | ID indice
    '''
    if len(p) == 2:
        p[0] = Tree('var', [], p[1])
    elif len(p) == 3:
        p[0] = Tree('var', [p[2]], p[1])

def p_indice(p):
    '''
    indice : indice ABRE_COL expressao FECHA_COL
            | ABRE_COL expressao FECHA_COL
    '''
    if len(p) == 5:
        p[0] = Tree('indice', [p[1], p[3]])
    elif len(p) == 4:
        p[0] = Tree('indice', [p[2]])

def p_tipo(p):
    '''
    tipo :  INTEIRO
            | FLUTUANTE
    '''
    p[0] = Tree('tipo',[],p[1])

def p_declaracao_funcao(p):
    '''
    declaracao_funcao : tipo cabecalho
                        | cabecalho
    '''
    if len(p) == 3:
        p[0] = Tree('declaracao_funcao', [p[1], p[2]])
    elif len(p) == 2:
        p[0] = Tree('declaracao_funcao', [p[1]])

def p_vazio(p):
    '''
    vazio : 
    '''
    p[0] = Tree('vazio',[])

def p_cabecalho(p):
    '''
    cabecalho : ID ABRE_PAR lista_parametros FECHA_PAR corpo FIM
    '''
    p[0] = Tree('cabecalho', [p[3], p[5]], p[1])

def p_lista_parametros(p):
    '''
    lista_parametros : lista_parametros VIRGULA parametro
                        | parametro
                        | vazio
    '''
    if len(p) == 4:
        p[0] = Tree('lista_parametros', [p[1], p[3]])
    elif len(p) == 2:
        p[0] = Tree('lista_parametros', [p[1]])

def p_parametro(p):
    '''
    parametro : tipo DOIS_PONTOS ID
                | parametro ABRE_COL FECHA_COL
    '''
    p[0] = Tree('parametro', [p[1]], p[3])

def p_corpo(p):
    '''
    corpo : corpo acao
            | vazio
    '''
    if len(p) == 3:
        p[0] = Tree('corpo', [p[1], p[2]])
    elif len(p) == 2:
        p[0] = Tree('corpo', [p[1]])

def p_acao(p):
    '''
    acao : expressao
            | declaracao_variaveis
            | se
            | repita
            | leia
            | escreva
            | retorna
            | error

    '''
    p[0] = Tree('acao', [p[1]])

def p_se(p):
    '''
    se : SE expressao ENTAO corpo FIM
        | SE expressao ENTAO corpo SENAO corpo FIM
    '''
    if len(p) == 6:
        p[0] = Tree('se', [p[2], p[4]])
    elif len(p) == 8:
        p[0] = Tree('se', [p[2], p[4], p[6]])

def p_repita(p):
    '''
    repita : REPITA corpo ATE expressao
    '''
    p[0] = Tree('repita', [p[2], p[4]])

def p_atribuicao(p):
    '''
    atribuicao : var ATRIBUICAO expressao 
    '''
    p[0] = Tree('atribuicao', [p[1],p[3]])

def p_leia( p):
    '''
    leia : LEIA ABRE_PAR var FECHA_PAR
    '''
    p[0] = Tree('leia', [], p[3])
    
def p_escreva( p):
    '''
    escreva : ESCREVA ABRE_PAR expressao FECHA_PAR
    '''
    p[0] = Tree('escreva', [], p[3])

def p_retorna( p):
    '''
    retorna : RETORNA ABRE_PAR expressao FECHA_PAR
    '''
    p[0] = Tree('retorna', [p[3]])

def p_expressao( p):
    '''
    expressao : expressao_logica
                | atribuicao
    '''
    p[0] = Tree('expressao', [p[1]])

def p_expressao_logica( p):
    '''
    expressao_logica : expressao_simples
                        | expressao_logica operador_logico expressao_simples
    '''
    if len(p) == 2:
        p[0] = Tree('expressao_logica', [p[1]])
    elif len(p) == 4:
        p[0] = Tree('expressao_logica', [p[1], p[2], p[3]])
        
def p_expressao_simples( p):
    '''
    expressao_simples : expressao_aditiva
                        | expressao_simples operador_relacional expressao_aditiva
    '''
    if len(p) == 2:
        p[0] = Tree('expressao_simples', [p[1]])
    elif len(p) == 4:
        p[0] = Tree('expressao_simples', [p[1], p[2], p[3]])

def p_expressao_aditiva(p):
    '''
    expressao_aditiva : expressao_multiplicativa
                        | expressao_aditiva operador_soma expressao_multiplicativa
    '''
    if len(p) == 2:
        p[0] = Tree('expressao_aditiva', [p[1]])
    elif len(p) == 4:
        p[0] = Tree('expressao_aditiva', [p[1], p[2], p[3]])

def p_expressao_multiplicativa( p):
    '''
    expressao_multiplicativa : expressao_unaria
                    | expressao_multiplicativa operador_multiplicacao expressao_unaria
    '''
    if len(p) == 2:
        p[0] = Tree('expressao_multiplicativa', [p[1]])
    elif len(p) == 4:
        p[0] = Tree('expressao_multiplicativa', [p[1], p[2], p[3]])

def p_expressao_unaria( p):
    '''
    expressao_unaria : fator
                    | operador_soma fator
                    | operador_negacao fator
    '''
    if len(p) == 2:
        p[0] = Tree('expressao_unaria', [p[1]])
    elif len(p) == 3:
        p[0] = Tree('expressao_unaria', [p[1], p[2]])

def p_operador_negacao(p):
    '''
    operador_negacao : NEGACAO
    '''
    p[0] = Tree('operador_negacao', [], p[1])

def p_operador_relacional( p):
    '''
    operador_relacional : MENOR
                        | MAIOR
                        | IGUALDADE
                        | DIFERENCA
                        | MENOR_IGUAL
                        | MAIOR_IGUAL
    '''
    p[0] = Tree('operador_relacional', [],p[1])

def p_operador_soma( p):
    '''
    operador_soma : SOMA
                | SUBTRACAO
    '''
    p[0] = Tree('operador_soma', [], p[1])

def p_operador_multiplicacao( p):
    '''
    operador_multiplicacao : MULTIPLICACAO
                            | DIVISAO
    '''
    p[0] = Tree('operador_multiplicacao', [], p[1])

def p_operador_logico(p):
    '''
    operador_logico : E_LOGICO
                | OU_LOGICO
    ''' 
    p[0] = Tree('operador_logico', [],p[1])

def p_fator(p):
    '''
    fator : ABRE_PAR expressao FECHA_PAR
          | var
          | chamada_funcao
          | numero
    '''
    if len(p) == 4:
            p[0] = Tree('fator', [p[2]])
    elif len(p) == 2:
        p[0] = Tree('fator', [p[1]])

def p_numero(p):
    '''
    numero : NUM_INTEIRO
            | NUM_FLUTUANTE
            | NUM_NOTACAO_CIENTIFICA
    '''
    p[0] = Tree('numero', [], p[1])

def p_chamada_funcao(p):
    '''
    chamada_funcao : ID ABRE_PAR lista_argumentos FECHA_PAR
    '''
    p[0] = Tree('chamada_funcao', [p[3]], p[1])

def p_lista_argumentos(p):
    '''
    lista_argumentos : lista_argumentos VIRGULA expressao
                       | expressao
                       | vazio
    '''
    if len(p) == 4:
        p[0] = Tree('lista_argumentos', [p[1], p[3]])
    elif len(p) == 2:
        p[0] = Tree('lista_argumentos', [p[1]])

def p_error(p):
    global contemErros
    contemErros = True

    colorama.init()
    if(p != None):
        data = abreArquivo()
        linha = p.lineno
    
        if(not linhasErros.__contains__(linha)):
            linhasErros.append(linha)
            print(colorama.Fore.LIGHTYELLOW_EX + "  File: '{0}', line: {1}".format(sys.argv[0],  linha))
            print(colorama.Fore.LIGHTRED_EX + "          " + data[linha - 1].replace(' ',''), colorama.Style.RESET_ALL)          
        parser.errok()
    else:
        print(colorama.Fore.LIGHTYELLOW_EX + "  Syntax error at EOF")

    
def abreArquivo():
    arq = open(sys.argv[1], 'r', encoding='utf-8')
    data = arq.readlines()
    return data


parser = yacc.yacc()
