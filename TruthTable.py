import re


class truthTable(object):

    def __init__(self, parameters, expressions=None):
        self.par = parameters
        self.expr = self.par + expressions
        self.condition = {}
        self.storage = []
        self.patternMatch = re.compile(r'(?<!\w)(' + '|'.join(self.par) + ')(?!\w)')
        # print(self.patternMatch)

    def calculateTable(self, currentIndex):
        if (currentIndex == len(self.par)):
            row = []
            for i in self.expr:
                tempExpression = i
                # print(i)
                tempExpression = self.patternMatch.sub(r"{\1}", tempExpression)
                # print(tempExpression)
                try:
                    row.append(eval(tempExpression.format(**self.condition)))
                except:
                    raise Exception("InvalidExpression")
            self.storage.append(row)
        else:
            self.condition[self.par[currentIndex]] = True
            self.calculateTable(currentIndex + 1)
            self.condition[self.par[currentIndex]] = False
            self.calculateTable(currentIndex + 1)

    def getTable(self):
        # print(self.expr)
        self.calculateTable(0)
        return self.storage


class stringConverter(object):
    def __init__(self, inputString):
        if (inputString == ""):
            raise Exception("A non-empty logic expression is required.")
        self.s = inputString + " "
        self.dict = {"/\\": "and", "\\/": "or", "->": "->", "<=>": "=="}
        self.operators = [r"/\\", r"\\/", r"->", r"<=>"]
        self.patternMatch = re.compile(r'(?<!\w)(' + '|'.join(self.operators) + ')(?!\w)')
        self.convertedExpression = self.patternMatch.sub(r"{\1}", self.s).format(**self.dict)
        self.convertedExpression = re.sub(r'\(', r'ProtectedLeftBracket(', self.convertedExpression)
        self.convertedExpression = re.sub(r'\)', r')ProtectedRightBracket', self.convertedExpression)
        self.convertedExpression = re.sub("(\w+) -> (\w+)", "not \g<1> or \g<2>", self.convertedExpression)
        self.convertedExpression = re.sub(r'ProtectedLeftBracket', r'', self.convertedExpression)
        self.convertedExpression = re.sub(r'ProtectedRightBracket', r'', self.convertedExpression)
        self.convertedExpression = self.convertedExpression.replace("~", "not ")

    def getConvertedExpression(self):
        return self.convertedExpression

    def getParameters(self):
        expressionNoOperators = self.patternMatch.sub(r"", self.s)
        expressionNoOperators = re.sub(r'\(', "", expressionNoOperators)
        expressionNoOperators = re.sub(r'\)', "", expressionNoOperators)
        # print(expressionNoOperators)
        paramters = []
        for i in range(1, len(expressionNoOperators)):
            if (expressionNoOperators[i] == ' ' and expressionNoOperators[i - 1] != ' '):
                j = i - 1
                paramterName = ""
                while (expressionNoOperators[j] != ' ' and expressionNoOperators[j] != '('):
                    if (expressionNoOperators[j] != ')' and expressionNoOperators[j] != '~'):
                        paramterName = expressionNoOperators[j] + paramterName
                    j = j - 1
                    if (j < 0):
                        break
                if (not (paramterName in paramters)):
                    paramters.append(paramterName)
        return paramters


# logicExpression = stringConverter("a -> ((b \\/ ~(c <=> (d -> (e /\\ f))))) ")
# # print(logicExpression.getParameters(), ' ', logicExpression.getConvertedExpression())
# for i in truthTable(logicExpression.getParameters(), [logicExpression.getConvertedExpression()]).getTable():
#     print(i)
