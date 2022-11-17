import sly
import pyexp_parser
import sys
import pyexp_lexer

#simple function to generate "temporary" variables
tmp_var_id_count = -1
def generate_tmp_var():
    global tmp_var_id_count
    tmp_var_id_count += 1
    return f't{tmp_var_id_count}'

#returns a tuple, the first element contains the name of the variable
#the expression is stored or the expression itself if it is a literal.
#the second element contains the list of statements that calculates the value stored in this variable.
def translate(exp):
    if type(exp) == tuple:
        if exp[0] == '=': #assignment node has the form ('=', ID, assigned)
            name = exp[1] #the expression is going to be stored in the identifier in the assignment.
            #no need to create a tmp variable!

            assigned_name, assigned_code = translate(exp[2])
            
            assigned_code.append(f'{name} = {assigned_name}')
            #calculate the value for the assigned and simply assign it to ID!

            code = assigned_code

        elif exp[0] == 'if': #if node has the form ('if', condition, ifbranch, elsebranch)
            name = generate_tmp_var()

            condition_name, condition_code = translate(exp[1])
            ifbranch_name, ifbranch_code = translate(exp[2])
            elsebranch_name, elsebranch_code = (None,[]) if (exp[3] == None) else translate(exp[3])
            #if the elsebranch does not exist, treat it as a None literal

            ifbranch_code = ["    "+stmt for stmt in ifbranch_code] #prepend with 4 spaces for if scope :)
            elsebranch_code = ["    "+stmt for stmt in elsebranch_code]

            condition_code.append(f'if {condition_name}:') #if condition is truthy...
            condition_code.extend(ifbranch_code) # calculate the value in the if branch...
            condition_code.append(f'    {name} = {ifbranch_name}')
            #and assign it to the tmp variable for this if_expression. (Don't forget the 4 spaces!)
            condition_code.append(f'else:') #otherwise...
            condition_code.extend(elsebranch_code) #calculate the value in the else branch...
            condition_code.append(f'    {name} = {elsebranch_name}')
            #and assign it to the tmp variable for this if_expression.

            code = condition_code

        elif exp[0] in ('+','-','//','*','=='): #binary op node has the form (op, firstarg, secondarg)
            name = generate_tmp_var()

            firstarg_name, firstarg_code = translate(exp[1])
            secondarg_name, secondarg_code = translate(exp[2])

            firstarg_code.extend(secondarg_code) #calculate(evaluate) firstarg, THEN secondarg.
            #very important line, has important semantic implications!

            firstarg_code.append(f'{name} = {firstarg_name} {exp[0]} {secondarg_name}')
            #do the operation and assign it to tmp variable for this op_expression.

            code = firstarg_code
        else:
            print(f'erroneous exp: {exp}')

        return (name, code)
    else: # it is a literal
        return (exp,[])

#simple function to insert newlines between generated code,
#wont put a new line if generated code is empty
def concat(str_list):
    return '\n'.join(filter(lambda x: x, str_list))


l = pyexp_lexer.PyExpLexer()
p = pyexp_parser.PyExpParser()

code = []
for exp in p.parse(l.tokenize(sys.stdin.read())):
    print('\n'.join(filter(lambda x: x, translate(exp)[1])),end='\n\n')