from TruthTable_ import expressionHandler
import re

def replace_operators(string):
    # Define the regular expressions and their corresponding replacements
    patterns = [
        (r'/\\|\b(and)\b', '&'),
        (r'\\/|\b(or)\b', '|'),
        (r'~|\b(not)\b', '!'),
        (r'->', '=>')
    ]
        # Apply the replacements to the string
    for pattern, replacement in patterns:
        string = re.sub(pattern, replacement, string)
    return string


class TruthTableHandler(object):

    def __init__(self, parameters, truthTable):
        self.parameters = parameters
        self.truthTable = truthTable
        self.tableConstruct = []
        for i in self.truthTable:
            temp = {}
            for j in range(len(i)):
                temp[self.parameters[j]] = i[j]
            self.tableConstruct.append(temp)

    def isSame(self, parameters, truthTable):
        if (len(parameters) != len(self.parameters)):
            return False
        for i in parameters:
            if (i not in self.parameters):
                return False
        for i in self.parameters:
            if (i not in parameters):
                return False
        for i in self.tableConstruct:
            if (i not in truthTable):
                return False
        return True

class ExpressionChecker(object):

    def __init__(self, user_input):
        user_input = replace_operators(user_input)
        self.original_expression = user_input
        self.expression = expressionHandler(user_input)
        self.parameters = self.expression.getVariables()
        self.truthTable = self.expression.getTruthtable()

    def isValid(self, s):
        try:
            temp = expressionHandler(s)
        except:
            print("Invalid expression: " + s)
            return False
        return True

    def isCorrect(self, s):
        try:
            temp = expressionHandler(s)
        except:
            return False
        parameters = temp.getParameters()
        truthTable = temp.getTruthTable()
        if (len(parameters) != len(self.parameters)):
            return False
        for i in parameters:
            if (i not in self.parameters):
                return False
        for i in self.parameters:
            if (i not in parameters):
                return False
        for i in truthTable:
            if (i not in self.truthTable):
                return False
        return True

    def isDNF(self):
        self.original_expression = self.original_expression.replace(" ", "")
        if (not self.isValid(self.original_expression)):
            return False
        conjunctions = self.original_expression.split("|")
        for i in conjunctions:
            expression = "".join(c for c in i if c not in ["!", "(", ")"]).split("&")
            for j in expression:
                if (j not in self.parameters):
                    return False
        return True