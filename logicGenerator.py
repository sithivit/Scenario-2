from DNFGenerator import DNFGenerator
from tabulate import tabulate


def replace_character(string, old, new):
    copy = ""
    for i in string:
        if i == old:
            copy += new
        else:
            copy += i
    return copy

def get_answer_validation(question):
    print(question)
    sample = []
    DNF = DNFGenerator(question)

    num_parameters = len(DNF.parameters)
    expression = DNF.generateDNF()

    parameters = DNF.parameters
    possible_conditions = [bin(i).replace("0b", "") for i in range(2**num_parameters)]
    possible_conditions = [(num_parameters-len(i))*'0' + i for i in possible_conditions]
    for i in possible_conditions:
        condition = [*i]
        variable_condition = zip(parameters, condition)
        temp = expression
        for i, j in variable_condition:
            temp = replace_character(temp, i, j)
        sample.append(bool(eval(temp)))


    valid = True
    for i in sample:
        if i == False:
            valid = False
    return valid

def get_answer_satisfy(question):
    print(question)
    sample = []
    DNF = DNFGenerator(question)

    num_parameters = len(DNF.parameters)
    expression = DNF.generateDNF()

    parameters = DNF.parameters
    possible_conditions = [bin(i).replace("0b", "") for i in range(2**num_parameters)]
    possible_conditions = [(num_parameters-len(i))*'0' + i for i in possible_conditions]
    for i in possible_conditions:
        condition = [*i]
        variable_condition = zip(parameters, condition)
        temp = expression
        for i, j in variable_condition:
            temp = replace_character(temp, i, j)
        sample.append(bool(eval(temp)))

    satisfy = False
    for i in sample:
        if i == True:
            valid = True
    return satisfy


def get_table(question):
    DNF = DNFGenerator(question)
    parameters = DNF.parameters
    DNFExpression = DNF.generateDNF()
    len_parameters = len(parameters)

    table = [[i for i in parameters]+[question]]
    possible_conditions = [bin(i).replace("0b", "") for i in range(2 ** len_parameters)]
    possible_conditions = [(len_parameters - len(i)) * '0' + i for i in possible_conditions]
    answers = []
    for i in possible_conditions:
        condition = [*i]
        table.append(condition+[' '])
        variable_condition = zip(parameters, condition)
        temp = DNFExpression
        for i, j in variable_condition:
            temp = replace_character(temp, i, j)
        answers.append(bool(eval(temp)))
    print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))
    return tabulate(table, headers='firstrow', tablefmt='fancy_grid'), answers
