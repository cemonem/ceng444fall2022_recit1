Repository for files in CENG444 Compilers course, Sly.py Recitation, 2022 Fall.

PyExp is a toy language that contains simple python binary operator expressions <code>+, -, *, //, ==</code> with only integer literals, variables, assignment, and the ternary if-else expression.
It also contains the if expression:

    ID = if exp

equivalent to

    ID = if exp else None

to contrast the dangling-else problem.

Features of sly.py are demonstrated to translate PyExp into TAC-like working Python code.

Newly added example: Breakwhile, a language with mock statements wrapped with ifs and whiles. Breaks and whiles are matched in translate.py