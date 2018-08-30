from lex import lexer
# Test it out

arq = open('teste.txt','r', encoding='utf-8')
data = arq.read()
print(data)
arq.close()

# Give the lexer some input
lexer.input(data)
# Tokenize
i = 0
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(i,"-",tok)
    i+=1