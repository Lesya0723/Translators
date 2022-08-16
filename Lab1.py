import json

SERVICE_WORDS = ['do', 'else', 'elsif', 'for', 'foreach', 'goto', 'if', 'print', 'return', 'sub', 'while']
OPERATIONS = ['!=', '%', '%=', '*', '**', '**=', '*=', '+', '++', '+=', '-', '--', '-=', '..', '/', '/=', '<', '<=', '=', '==', '>', '>=', 'and', 'not', 'or']
SEPARATORS = ['\n', ' ', '(', ')', ',', ';', '[', ']', '{', '}']

def check(tokens, token_class, token_value):
    if not(token_value in tokens[token_class]):
        token_code = str(len(tokens[token_class]) + 1)
        tokens[token_class][token_value] = token_class + token_code

def get_operation(input_sequence, i):
    for k in range(3, 0, -1):
        if i + k < len(input_sequence):
            buffer = input_sequence[i:i + k]
            if buffer in OPERATIONS:
                return buffer
    return ''

def get_separator(input_sequence, i):
    buffer = input_sequence[i]
    if buffer in SEPARATORS:
        return buffer
    return ''

# лексемы
tokens = {'W': {}, 'I': {}, 'O': {}, 'R': {}, 'N': {}, 'C': {}}

for service_word in SERVICE_WORDS:
    check(tokens, 'W', service_word)
for operation in OPERATIONS:
    check(tokens, 'O', operation)
for separator in SEPARATORS:
    check(tokens, 'R', separator)

# файл, содержащий текст на входном языке программирования
f = open('perl.txt', 'r')
input_sequence = f.read()
f.close()

i = 0
state = 'S'
output_sequence = buffer = ''
while i < len(input_sequence):
    symbol = input_sequence[i]
    operation = get_operation(input_sequence, i)
    separator = get_separator(input_sequence, i)
    if state == 'S':
        buffer = ''
        if symbol.isalpha():
            state = 'q1'
            buffer += symbol
        elif symbol in ['$', '&', '@', '_']:
            state = 'q2'
            buffer += symbol
        elif symbol.isdigit():
            state = 'q3'
            buffer += symbol
        elif symbol == "'":
            state = 'q9'
            buffer += symbol
        elif symbol == '"':
            state = 'q10'
            buffer += symbol
        elif symbol == '#':
            state = 'q11'
        elif operation:
            check(tokens, 'O', operation)
            output_sequence += tokens['O'][operation] + ' '
            i += len(operation) - 1
        elif separator:
            if separator != ' ':
                check(tokens, 'R', separator)
                output_sequence += tokens['R'][separator]
                if separator == '\n':
                    output_sequence += '\n'
                else:
                    output_sequence += ' '
        elif i == len(input_sequence) - 1:
            state = 'Z'
    elif state == 'q1':
        if symbol.isalpha():
            buffer += symbol
        elif symbol.isdigit():
            state = 'q2'
            buffer += symbol
        else:
            if operation or separator:
                if buffer in SERVICE_WORDS:
                    output_sequence += tokens['W'][buffer] + ' '
                elif buffer in OPERATIONS:
                    output_sequence += tokens['O'][buffer] + ' '
                else:
                    check(tokens, 'I', buffer)
                    output_sequence += tokens['I'][buffer] + ' '
                if operation:
                    check(tokens, 'O', operation)
                    output_sequence += tokens['O'][operation] + ' '
                    i += len(operation) - 1
                if separator:
                    if separator != ' ':
                        check(tokens, 'R', separator)
                        output_sequence += tokens['R'][separator]
                        if separator == '\n':
                            output_sequence += '\n'
                        else:
                            output_sequence += ' '
            state = 'S'
    elif state == 'q2':
        if symbol == '_' or symbol.isalpha() or symbol.isdigit():
            buffer += symbol
        else:
            if operation or separator:
                check(tokens, 'I', buffer)
                output_sequence += tokens['I'][buffer] + ' '
 
                if operation:
                    check(tokens, 'O', operation)
                    output_sequence += tokens['O'][operation] + ' '
                    i += len(operation) - 1
                if separator:
                    if separator != ' ':
                        check(tokens, 'R', separator)
                        output_sequence += tokens['R'][separator]
                        if separator == '\n':
                            output_sequence += '\n'
                        else:
                            output_sequence += ' '
                state = 'S'
    elif state == 'q3':
        if symbol.isdigit():
            buffer += symbol
        elif symbol == '.':
            state = 'q4'
            buffer += symbol
        elif symbol == 'e' or symbol == 'E':
            state = 'q6'
            buffer += symbol
        else:
            if operation or separator:
                check(tokens, 'N', buffer)
                output_sequence += tokens['N'][buffer] + ' '
                if operation:
                    check(tokens, 'O', operation)
                    output_sequence += tokens['O'][operation] + ' '
                    i += len(operation) - 1
                if separator:
                    if separator != ' ':
                        check(tokens, 'R', separator)
                        output_sequence += tokens['R'][separator]
                        if separator == '\n':
                            output_sequence += '\n'
                        else:
                            output_sequence += ' '
                state = 'S'
    elif state == 'q4':
        if symbol.isdigit():
            state = 'q5'
            buffer += symbol
    elif state == 'q5':
        if symbol.isdigit():
            buffer += symbol
        elif symbol == 'e' or symbol == 'E':
            state = 'q6'
            buffer += symbol
        else:
            if operation or separator:
                check(tokens, 'N', buffer)
                output_sequence += tokens['N'][buffer] + ' '
                if operation:
                    check(tokens, 'O', operation)
                    output_sequence += tokens['O'][operation] + ' '
                    i += len(operation) - 1
                if separator:
                    if separator != ' ':
                        check(tokens, 'R', separator)
                        output_sequence += tokens['R'][separator]
 
                        if separator == '\n':
                            output_sequence += '\n'
                        else:
                            output_sequence += ' '
                state = 'S'
    elif state == 'q6':
        if symbol == '-' or symbol == '+':
            state = 'q7'
            buffer += symbol
        elif symbol.isdigit():
            state = 'q8'
            buffer += symbol
    elif state == 'q7':
        if symbol.isdigit():
            state = 'q8'
            buffer += symbol
    elif state == 'q8':
        if symbol.isdigit():
            buffer += symbol
        else:
            if operation or separator:
                check(tokens, 'N', buffer)
                output_sequence += tokens['N'][buffer] + ' '
                if operation:
                    check(tokens, 'O', operation)
                    output_sequence += tokens['O'][operation] + ' '
                    i += len(operation) - 1
                if separator:
                    if separator != ' ':
                        check(tokens, 'R', separator)
                        output_sequence += tokens['R'][separator]
                        if separator == '\n':
                            output_sequence += '\n'
                        else:
                            output_sequence += ' '
            state = 'S'
    elif state == 'q9':
        if symbol != "'":
            buffer += symbol
        elif symbol == "'":
            buffer += symbol
            check(tokens, 'C', buffer)
            output_sequence += tokens['C'][buffer] + ' '
            state = 'S'
    elif state == 'q10':
        if symbol != '"':
            buffer += symbol
        elif symbol == '"':
            buffer += symbol
            check(tokens, 'C', buffer)
            output_sequence += tokens['C'][buffer] + ' '
            state = 'S'
    elif state == 'q11':
        if symbol == '\n':
            state = 'S'
        elif i == len(input_sequence) - 1:
            state = 'Z'
    i += 1


 
# файлы, содержащие все таблицы лексем
for token_class in tokens.keys():
    with open('%s.json' % token_class, 'w') as write_file:
        data = {val: key for key, val in tokens[token_class].items()}
        json.dump(data, write_file, indent=4, ensure_ascii=False)

# файл, содержащий последовательность кодов лексем входной программы
f = open('tokens.txt', 'w')
f.write(output_sequence)
f.close()
