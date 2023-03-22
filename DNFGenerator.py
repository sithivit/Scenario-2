from TruthTable import expressionHandler

class DNFGenerator(object):

    def __init__(self, expression):
        self.expression = expression
        temp = expressionHandler(expression)
        self.parameters = temp.getParameters()
        self.truth_table = temp.getTruthtable()


    def generateDNF(self):
        dnf_expression = ""
        for row in self.truth_table:
            if row[-1]:  # If the result is True
                term = ""
                for col in range(len(row) - 1):
                    if row[col]:
                        term += self.parameters[col] + " and "
                    else:
                        term += "not " + self.parameters[col] + " and "
                term = "(" + term[0:-5] + ")"
                dnf_expression += term + " or "

        return dnf_expression[0:-3]
