from lex import lexer

arq = open('./lexica-testes/bubble_sort.tpp','r', encoding='utf-8')
#arq = open('./lexica-testes/Busca_Linear_1061992.tpp','r', encoding='utf-8')
#arq = open('./lexica-testes/fat.tpp','r', encoding='utf-8')
#arq = open('./lexica-testes/multiplicavetor.tpp','r', encoding='utf-8')
#arq = open('./lexica-testes/primo.tpp','r', encoding='utf-8')
#arq = open('./lexica-testes/somavet.tpp','r', encoding='utf-8')
#arq = open('./lexica-testes/teste-1.tpp','r', encoding='utf-8')
#arq = open('./lexica-testes/teste-2.tpp','r', encoding='utf-8')

data = arq.read()
arq.close()

lexer.input(data)
i = 0
while True:
    tok = lexer.token()
    if not tok: 
        break 
    print(i,"-",tok.type,tok.value, tok.lineno, tok.lexpos)      #print(tok.type, tok.value, tok.lineno, tok.lexpos)
    
    i+=1