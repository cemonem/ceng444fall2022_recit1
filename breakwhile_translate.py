import sly
import breakwhile_parser
import sys
import breakwhile_lexer

tmp_var_id_count = -1
def generate_label():
    global tmp_var_id_count
    tmp_var_id_count += 1
    return f'label{tmp_var_id_count}'

while_labels = {}
def translate(stmt, recent_while):
    if stmt == "break":
        if recent_while == None:
            return 'break out of ....uhhhhh semantic error :( ;'
        if recent_while not in while_labels:
            while_labels[recent_while] = generate_label()
        return f'break out of {while_labels[recent_while]};'
    elif type(stmt) == tuple:
        if stmt[0] == "while":
            inner = '\n'.join([indent(translate(stmts_in_this_while, stmt)) for stmts_in_this_while in stmt[1]]) #ATTENTION HERE!
            if stmt in while_labels:
                return '\n'.join([f'while({while_labels[stmt]})','{', inner,'}'])
            return '\n'.join(['while','{',inner,'}'])
        else:
            inner = '\n'.join([indent(translate(stmt_in_this_if, recent_while)) for stmt_in_this_if in stmt[1]])
            return '\n'.join(['if','{',inner,'}'])
    else:
        return stmt+';'

def indent(stmt_translation):
    return '\n'.join(["  "+elem for elem in stmt_translation.split('\n')])

l = breakwhile_lexer.BreakWhileLexer()
p = breakwhile_parser.BreakWhileParser()

for stmt in p.parse(l.tokenize(sys.stdin.read())):
    print(translate(stmt, None))
