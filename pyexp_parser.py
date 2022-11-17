import sly
import pyexp_lexer

class PyExpParser(sly.Parser):
    tokens = pyexp_lexer.PyExpLexer.tokens
    debugfile = 'pyexp_parser.out'

    precedence = (
        ('left', EQ),
        ('left', '+','-'),
        ('left', '*', DIVIDE)
    )

    @_('newline_opt')
    def program(self, p):
        return []

    @_('newline_opt exps newline_opt')
    def program(self, p):
        return p.exps

    @_('exps NEWLINE exp')
    def exps(self, p):
        p[0].append(p[2])
        return p[0]

    @_('exp')
    def exps(self, p):
        return [p[0]]

    @_('assign')
    def exp(self, p):
        return p[0]

    @_('ID ASSIGN assign')
    def assign(self, p):
        return ('=', p[0], p[2])

    @_('if_exp')
    def assign(self, p):
        return p[0]

    @_('term IF exp')
    def if_exp(self, p):
        return ('if', p[2], p[0], None)

    @_('term IF exp ELSE exp')
    def if_exp(self, p):
        return ('if', p[2], p[0], p[4])

    @_('term')
    def if_exp(self, p):
        return p[0]

    @_('term "+" term',
       'term "-" term',
       'term DIVIDE term',
       'term "*" term',
       'term EQ term')
    def term(self, p):
        return (p[1], p[0], p[2])

    @_('"(" exp ")"')
    def term(self, p):
        return p[1]

    @_('NUMBER','ID')
    def term(self, p):
        return p[0]

    @_('NEWLINE','empty')
    def newline_opt(self, p):
        pass

    @_('')
    def empty(self, p):
        pass
