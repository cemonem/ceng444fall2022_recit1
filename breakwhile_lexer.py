import sly

class BreakWhileLexer(sly.Lexer):
    tokens = {IF, WHILE, BREAK, ID}

    ignore = ' \t'
    ignore_comment = r'\#.*'

    literals = {';','{','}'}

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    ID['if'] = IF
    ID['while'] = WHILE
    ID['break'] = BREAK

    @_('\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value) #have to manually increment it
        return t

    def error(self, t):
        print('Bad character %r' % (t.value[0]))
        self.index += 1 #for some reason you need to update this
        #otherwise goes into inf loop
        t.value = t.value[0] #returns error token.
        return t
