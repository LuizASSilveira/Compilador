import ply.lex as lex

# List of token names.   This is always required
reserved = {
    'inteiro':'INTEIRO',
    'se':'SE',
    'então':'ENTAO',
    'senão':'SENAO',
    'fim':'FIM',
    'repita':'REPITA',
    'flutuante':'FLUTUANTE',
    'retorna':'RETORNA',
    'até':'ATE',
    'leia':'LEIA', 
    'escreva':'ESCREVA',
}
tokens = [
    'SOMA',
    'SUBTRACAO',
    'MULTIPLICACAO',
    'DIVISAO',
    'ABREPAR',
    'FECHAPAR',
    'IGUALDADE',
    'VIRGULA',
    'ATRIBUICAO',
    'MENOR',
    'MAIOR',
    'MENORIGUAL',
    'MAIORIGUAL',
    'DOISPONTOS',
    'ABRECOL',
    'FECHACOL',
    'ELOGICO',
    'OULOGICO',
    'NEGACAO',
    'NUMERO',
    'IDENTIFICADOR',

] +  list(reserved.values())

# Regular expression rules for simple tokens
t_SOMA    = r'\+'
t_SUBTRACAO   = r'-'
t_MULTIPLICACAO   = r'\*'
t_DIVISAO  = r'/'
t_ABREPAR  = r'\('
t_FECHAPAR  = r'\)'
t_IGUALDADE = r'\='
t_VIRGULA = r'\,'
t_ATRIBUICAO = r'\:\='
t_MENORIGUAL = r'\<\='
t_MAIORIGUAL = r'\=\>'
t_MENOR = r'\<'
t_MAIOR = r'\>'
t_DOISPONTOS = r'\:'
t_ABRECOL = r'\['
t_FECHACOL = r'\]'
t_ELOGICO = r'\&\&'
t_OULOGICO = r'\|\|'
t_NEGACAO = r'\!'



# t_FLUTUANTE = r'flutuante'
# t_INTEIRO = r'inteiro'
# t_SE = r'se'
# t_ENTAO = r'(entà-úo)'
# t_SENAO = r'senão'
# t_FIM = r'fim'
# t_REPITA = r'repita'
# t_RETORNA = r'retorna'
# t_ATE = r'até'
# t_LEIA = r'leia'
# t_ESCREVA = r'escreve' 


# A regular expression rule with some action code
def t_NUMERO(t):
    r'[0-9]+(\.[0-9]+)?(E(\+|\-)?[0-9]+)?'
    t.value = str(t.value)    
    return t

def t_IDENTIFICADOR(t):
    r'([a-zA-Z])+[0-9]*'
    t.value = str(t.value)    
    return t
    
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words 
    return t


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_COMMENT(t):
    r'{(.|[\r\n])*}'
    pass
    #Token discarded    

lexer = lex.lex()