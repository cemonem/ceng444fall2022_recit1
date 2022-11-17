import sly
import pyexp_parser
import sys
import pyexp_lexer
l = pyexp_lexer.PyExpLexer()
p = pyexp_parser.PyExpParser()
for exp in p.parse(l.tokenize(sys.stdin.read())):
    print(exp)
