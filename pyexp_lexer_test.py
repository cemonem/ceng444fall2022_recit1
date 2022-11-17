from pyexp_lexer import *
import sys

l = PyExpLexer()
for tok in l.tokenize(sys.stdin.read()):
    print(tok)