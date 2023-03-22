import random

variables = ['p', 'q', 'r', 's']
operators = ['&', '|', '~']

def generate_expression(max_variables):
    if max_variables == 0:
        return random.choice(variables)
    else:
        operator = random.choice(operators)
        if operator == '~':
            sub_expression = generate_expression(max_variables-1)
            if sub_expression[0] == '~':
                sub_expression = sub_expression[1:]
            else:
                sub_expression = '~' + sub_expression
            return sub_expression
        else:
            sub_expression1 = generate_expression(max_variables-1)
            sub_expression2 = generate_expression(max_variables-1)
            if sub_expression1[0] == '~' and sub_expression2[0] == '~':
                operator = '|' if operator == '&' else '&'
                sub_expression1 = sub_expression1[1:]
                sub_expression2 = sub_expression2[1:]
            elif sub_expression1[0] == '~':
                sub_expression1 = sub_expression1[1:]
                sub_expression1, sub_expression2 = sub_expression2, sub_expression1
            elif sub_expression2[0] == '~':
                sub_expression2 = sub_expression2[1:]
            return sub_expression1 + operator + sub_expression2

def generate_solvable_expression(max_variables):
    while True:
        expression = generate_expression(max_variables)
        if eval(expression, {}, {}):
            return expression

expression = generate_solvable_expression(3)
print(expression)
