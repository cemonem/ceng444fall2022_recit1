import sly

class PyExpLexer(sly.Lexer):
    tokens = {ID, NUMBER, ASSIGN, EQ, DIVIDE, IF, ELSE, NEWLINE}

    ignore = ' \t'
    ignore_comment = r'\#[^\n]*'

    literals = {'(',')','+','-','*'}

    DIVIDE = '//'
    EQ = '=='
    ASSIGN = '=' #longer rules first!

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t
    
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['else'] = ELSE

    @_('\n+')
    def NEWLINE(self, t):
        self.lineno += len(t.value) #have to manually increment it
        return t

    def error(self, t):
        print('Bad character %r' % (t.value[0]))
        self.index += 1 #for some reason you need to update this
        #otherwise goes into inf loop
        return t #returns error token.
