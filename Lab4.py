import lab1
import json
import re
import sys

# лексемы
tokens = {'W': {}, 'I': {}, 'O': {}, 'R': {}, 'N': {}, 'C': {}}

# файлы, содержащие все таблицы лексем
for token_class in tokens.keys():
    with open('%s.json' % token_class, 'r') as read_file:
        data = json.load(read_file)
        tokens[token_class] = data

# файл, содержащий последовательность кодов лексем входной программы
f = open('tokens.txt', 'r')
input_sequence = f.read()
f.close()

regexp = '[' + '|'.join(tokens.keys()) + ']' + '\d+'
match = re.findall(regexp, input_sequence)

i = -1 # индекс разбираемого символа
nxtsymb = None # разбираемый символ
row_counter = 1 # счётчик строк

# обработка ошибочной ситуации
def error():
    print('Ошибка в строке', row_counter)
    sys.exit()

# помещение очередного символа в nxtsymb
def scan():
    global i, nxtsymb, row_counter
    i += 1
    if i >= len(match):
        if not(nxtsymb in ['\n', ';', '}']):
            error()
    else:
        for token_class in tokens.keys():
            if match[i] in tokens[token_class]:
                nxtsymb = tokens[token_class][match[i]]
        if nxtsymb == '\n':
            row_counter += 1
            scan()
        # print(i, row_counter, nxtsymb)

# программа
def program():
    operators()


 
# операторы
def operators():
    global i
    scan()
    while name() or \
          nxtsymb in ['{', 'sub', 'if', 'while', 'do', 'for', 'goto', 'break', \
                      'continue', 'return', 'print']:
        operator()
        if nxtsymb == ';':
            scan()
        if nxtsymb == '}':
            break

# оператор
def operator():
    if name():
        scan()
        if nxtsymb == ':':
            scan()
            operator()
        elif nxtsymb == '(':
            scan()
            expression()
            while nxtsymb == ',':
                scan()
                expression()
            if nxtsymb != ')': error()
            scan()
        elif nxtsymb == '[':
            scan()
            expression()
            if nxtsymb != ']': error()
            scan()
        elif nxtsymb == '=':
            scan()
            expression()
        else: error()
    elif nxtsymb == '{': compound_operator()
    elif nxtsymb == 'sub': function()
    elif nxtsymb == 'if': conditional_operator()
    elif nxtsymb == 'while': while_loop()
    elif nxtsymb == 'do': do_while_loop()
    elif nxtsymb == 'for': for_loop()
    elif nxtsymb == 'goto':
        goto_statement()
        scan()
    elif nxtsymb == 'break':
        break_operator()
        scan()
    elif nxtsymb == 'continue':
        continue_operator()
        scan()
    elif nxtsymb == 'return': return_operator()
    elif nxtsymb == 'print': print_operator()
    else: error()

# имя (идентификатор)
def name():
    return nxtsymb in tokens['I'].values()

 
# функция
def function():
    if nxtsymb != 'sub': error()
    scan()
    if not(name()): error()
    scan()
    compound_operator()

# выражение
def expression():
    if nxtsymb == '(':
        scan()
        expression()
        if nxtsymb != ')': error()
        scan()
    elif name():
        scan()
        if nxtsymb == '(':
            scan()
            expression()
            while nxtsymb == ',':
                scan()
                expression()
            if nxtsymb != ')': error()
            scan()
        elif nxtsymb == '[':
            scan()
            expression()
            while nxtsymb == ',':
                scan()
                expression()
            if nxtsymb != ']': error()
            scan()
    elif number() or line(): scan()
    else: error()
    if arithmetic_operation():
        scan()
        expression()

# число (числовая константа)
def number():
    return nxtsymb in tokens['N'].values()

# целое число (числовая константа)
def integer():
    return nxtsymb in tokens['N'].values()

# вещественное число (числовая константа)
def real_number():
    return nxtsymb in tokens['N'].values()

# строка (символьная константа)
def line():
    return nxtsymb in tokens['C'].values()


 
# переменная
def variable():
    if not(name()): error()
    scan()
    if nxtsymb == '[':
        scan()
        expression()
        if nxtsymb != ']': error()
        scan()

# арифметическая операция
def arithmetic_operation():
    return nxtsymb in ['%', '*', '**', '+', '-', '..', '/']

# составной оператор
def compound_operator():
    if nxtsymb != '{': error()
    operators()
    if nxtsymb != '}': error()
    scan()

# оператор присваивания
def assignment_operator():
    scan()
    variable()
    if nxtsymb != '=': error()
    scan()
    expression()

# условный оператор
def conditional_operator():
    if nxtsymb != 'if': error()
    scan()
    if nxtsymb != '(': error()
    condition()
    if nxtsymb != ')': error()
    scan()
    compound_operator()
    if nxtsymb == 'else':
        scan()
        compound_operator()

# условие
def condition():
    if unary_log_operation():
        scan()
        if nxtsymb != '(': error()
        log_expression()
        if nxtsymb != ')': error()
        scan()
    else:
        log_expression()
        while binary_log_operation():
            log_expression()

# унарная логическая операция
def unary_log_operation():
    return nxtsymb == 'not'


 
# логическое выражение
def log_expression():
    scan()
    expression()
    comparison_operation()
    scan()
    expression()

# операция сравнения
def comparison_operation():
    return nxtsymb in ['!=', '<', '<=', '==', '>', '>=']

# бинарная логическая операция
def binary_log_operation():
    return nxtsymb == 'and' or nxtsymb == 'or'

# цикл while
def while_loop():
    if nxtsymb != 'while': error()
    scan()
    if nxtsymb != '(': error()
    condition()
    if nxtsymb != ')': error()
    scan()
    compound_operator()

# цикл do while
def do_while_loop():
    if nxtsymb != 'do': error()
    scan()
    compound_operator()
    if nxtsymb != 'while': error()
    scan()
    if nxtsymb != '(': error()
    scan()
    condition()
    if nxtsymb != ')': error()

# цикл for
def for_loop():
    if nxtsymb != 'for': error()
    scan()
    if nxtsymb != '(': error()
    assignment_operator()
    if nxtsymb != ';': error()
    condition()
    if nxtsymb != ';': error()
    assignment_operator()
    if nxtsymb != ')': error()
    scan()
    compound_operator()

# оператор goto
def goto_statement():
    if nxtsymb != 'goto': error()
    scan()
    if not(name()): error()
    scan()


 
# оператор break
def break_operator():
    return nxtsymb == 'break'

# оператор continue
def continue_operator():
    return nxtsymb == 'continue'

# оператор return
def return_operator():
    if nxtsymb != 'return': error()
    scan()
    expression()

# оператор print
def print_operator():
    if nxtsymb != 'print': error()
    scan()
    expression()

program()
