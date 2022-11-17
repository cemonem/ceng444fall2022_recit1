import sly
import breakwhile_parser
import sys
import breakwhile_lexer
l = breakwhile_lexer.BreakWhileLexer()
p = breakwhile_parser.BreakWhileParser()
for stmt in p.parse(l.tokenize(sys.stdin.read())):
    print(stmt)
