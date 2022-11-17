import sly
import breakwhile_lexer

class BreakWhileParser(sly.Parser):
    tokens = breakwhile_lexer.BreakWhileLexer.tokens
    debugfile = 'breakwhile_parser.out'

    @_('stmts')
    def program(self, p):
        return tuple(p[0])
    
    @_('stmts stmt')
    def stmts(self, p):
        p[0].append(p[1])
        return p[0]
    
    @_('empty')
    def stmts(self, p):
        return []
    
    @_('error ";"')
    def stmt(self, p):
        return 'ERROR!'
    
    @_('ID ";"')
    def stmt(self, p):
        return p.ID
    
    @_('BREAK ";"')
    def stmt(self, p):
        return p.BREAK
    
    @_('IF "{" stmts "}"')
    def stmt(self, p):
        return ('if', tuple(p.stmts))
    
    @_('WHILE "{" stmts "}"')
    def stmt(self, p):
        return ('while', tuple(p.stmts))
    
    @_('')
    def empty(self, p):
        return