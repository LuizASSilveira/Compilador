import ply.lex as lex

#Palavras reservadas
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
# Lista com Tokens
tokens = [
    'SOMA',
    'SUBTRACAO',
    'MULTIPLICACAO',
    'DIVISAO',
    'ABRE_PAR',
    'FECHA_PAR',
    'IGUALDADE',
    'VIRGULA',
    'ATRIBUICAO',
    'MENOR',
    'MAIOR',
    'MENOR_IGUAL',
    'MAIOR_IGUAL',
    'DOIS_PONTOS',
    'ABRE_COL',
    'FECHA_COL',
    'E_LOGICO',
    'OU_LOGICO',
    'NEGACAO',
    'NUM_INTEIRO',
    'NUM_FLUTUANTE',
    'NUM_NOTACAO_CIENTIFICA',
    'ID',
    'DIFERENCA',
] +  list(reserved.values())

# Expressão Regular
t_SOMA    = r'\+'
t_SUBTRACAO   = r'-'
t_MULTIPLICACAO   = r'\*'
t_DIVISAO  = r'/'
t_ABRE_PAR  = r'\('
t_FECHA_PAR  = r'\)'
t_IGUALDADE = r'\='
t_VIRGULA = r'\,'
t_ATRIBUICAO = r'\:\='
t_MENOR_IGUAL = r'\<\='
t_MAIOR_IGUAL = r'\=\>'
t_MENOR = r'\<'
t_MAIOR = r'\>'
t_DOIS_PONTOS = r'\:'
t_ABRE_COL = r'\['
t_FECHA_COL = r'\]'
t_E_LOGICO = r'\&\&'
t_OU_LOGICO = r'\|\|'
t_NEGACAO = r'\!'
t_DIFERENCA = r'\<\>'

# literals = "+-*/"

t_ignore  = ' \t'                                #ingnorar caracters (spaces and tabs)

def t_COMMENT(t):                                #pegar comentarios e descartar o token
    r'\{[^}]*[^{]*\}'
    pass

def t_NUM_NOTACAO_CIENTIFICA(t):                # Expressão regular para numeros (int,float, notação cientifica)
    r'[0-9]+(\.*[0-9]*)(e(\+|\-| )[0-9]+)'
    return t

def t_NUM_FLUTUANTE(t):
    r'[0-9]+\.[0-9]*'
    t.value = float(t.value)    
    return t

def t_NUM_INTEIRO(t):
    r'[0-9]+'
    t.value = int(t.value)    
    return t

def t_ID(t):                                    #Expressão regular para identificadores
    r'[a-zA-Z_]+[a-zà-úA-ZÀ-Ú0-9_]*'
    t.type = reserved.get(t.value,'ID')    # procura por palavras reservadas 
    return t

# Mensagem de error
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Defina uma regra para rastrear o números de linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()