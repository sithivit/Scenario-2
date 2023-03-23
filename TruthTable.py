import re
from collections import defaultdict

def check_integrity(s):
    for i in s:
        if not re.match("[A-Za-z_0-9\\\/<>\-~()\s\&\|\=\!]", i):
            raise Exception("Illegal character")

def read_operator(s, index):
    # Single char operator
    if re.match("[()TF!&|]", s[index]):
        return s[index]

    if index == len(s) - 1:
        return None

    # 2 char operator; =>, or
    if s[index:index + 2] == "=>":
        return s[index:index + 2]

    if index == len(s) - 2:
        return None

    subs = s[index:index + 3]
    if subs == "<=>":
        return subs

    return None


def is_reserved_word(c):
    return c in ["!", "&", "|", "T", "F", "=>", "<=>"]


def read_variable(s, index):
    if not re.match("[A-Za-z]", s[index]):
        return None

    res = ""
    while index < len(s) and re.match("[A-Za-z]", s[index]):
        res += s[index]
        index += 1

    return res


def make_identity_token(s, index):
    return {"type": s, "start": index, "end": index + len(s)}


def make_variable_token(index, start, end):
    return {"type": "variable", "index": index, "start": start, "end": end}


def scan_variable(input, index, variableSet):
    var_name = read_variable(input, index)
    variableSet[var_name] = True
    return var_name


def preliminary_scan(input):
    variableSet = defaultdict(bool)
    i = 0
    tokens = []

    while (i <= len(input)):
        if i >= len(input):
            return {"tokens": tokens, "variableSet": variableSet}

        if read_variable(input, i):
            var = read_variable(input, i)
            variableSet[var] = True
            tokens.append(make_variable_token(var, i, i + len(var)))
            # print(make_variable_token(var, i, i + len(var)))
            i += len(var)

        elif read_operator(input, i):
            op = read_operator(input, i)
            tokens.append(make_identity_token(op, i))
            i += len(op)

        elif input[i] == " ":
            i += 1

        else:
            raise Exception("Invalid character " + input[i])


def number_variables(prelim_dict):
    vars = []
    for key in prelim_dict["variableSet"].keys():
        vars.append(key)

    vars.sort()

    for i in range(len(vars)):
        prelim_dict["variableSet"][vars[i]] = i

    for i in range(len(prelim_dict["tokens"])):
        if prelim_dict["tokens"][i]["type"] == "variable":
            prelim_dict["tokens"][i]["index"] = prelim_dict["variableSet"][prelim_dict["tokens"][i]["index"]]

    return {"tokens": prelim_dict["tokens"], "variables": vars}


def scan(input):
    preliminary_dict = preliminary_scan(input)
    return number_variables(preliminary_dict)


class TrueNode:
    def __init__(self):
        pass

    def evaluate(self):
        return True

    def toString(self):
        return "T"


class FalseNode:
    def __init__(self):
        pass

    def evaluate(self, assignment):
        return False

    def toString(self, variables):
        return "F"


class NegateNode:
    def __init__(self, underlying):
        self.underlying = underlying

    def evaluate(self, assignment):
        return not self.underlying.evaluate(assignment)

    def toString(self, variables):
        return " NOT " + self.underlying.toString(variables)


class AndNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) and self.right.evaluate(assignment)

    def toString(self, variables):
        return "(" + self.left.toString(variables) + " AND " + self.right.toString(variables) + ")"


class OrNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) or self.right.evaluate(assignment)

    def toString(self, variables):
        return "(" + self.left.toString(variables) + " OR " + self.right.toString(variables) + ")"


class ImpliesNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, assignment):
        return (not self.left.evaluate(assignment)) or self.right.evaluate(assignment)

    def toString(self, variables):
        return "(" + self.left.toString(variables) + " IMP " + self.right.toString(variables) + ")"


class IffNode:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def evaluate(self, assignment):
        return self.left.evaluate(assignment) == self.right.evaluate(assignment)

    def toString(self, variables):
        return "(" + self.left.toString(variables) + " IFF " + self.right.toString(variables) + ")"


class VariableNode:
    def __init__(self, index):
        self.index = index

    def evaluate(self, assignment):
        return assignment[self.index]

    def toString(self, variables):
        return variables[self.index]

def isOperand(token):
    return token["type"] == "T" or token["type"] == "F" or token["type"] == "variable"

def wrapOperand(token):
    if token["type"] == "T":
        return TrueNode()
    elif token["type"] == "F":
        return FalseNode()
    elif token["type"] == "variable":
        return VariableNode(token["index"])
    else:
        raise Exception("invalid operand for wrap")


def priority(token):
    return 0 if token["type"] == "<=>" else 1 if token["type"] == "=>" else 2 if token["type"] == "|" else 3 if token[
                                                                                                                    "type"] == "&" else -1 if \
    token["type"] == "$" else None


def isBinaryOperator(token):
    return token["type"] in ["<=>", "=>", "|", "&"]


def createOperatorNode(left, token, right):
    return IffNode(left, right) if token["type"] == "<=>" else ImpliesNode(left, right) if token[
                                                                                               "type"] == "=>" else OrNode(
        left, right) if token["type"] == "|" else AndNode(left, right) if token["type"] == "&" else None


def addOperand(node, operands, operators):
    while (len(operators) > 0 and operators[-1]["type"] == "!"):
        operators.pop(len(operators) - 1)
        node = NegateNode(node)
    operands.append(node)


def parse(input):
    scanResult = scan(input)
    tokens = scanResult["tokens"]
    tokens.append({'end': len(input), 'start': len(input), 'type': '$'})  # EOF Constant
    operators = []
    operands = []
    needOperand = True

    for t in tokens:
        if needOperand:
            if isOperand(t):
                addOperand(wrapOperand(t), operands, operators)
                needOperand = False

            elif t["type"] == "(" or t["type"] == "!":
                operators.append(t)  # operator stack

            elif t['type'] == '$':
                # end
                if len(operators) == 0:
                    raise Exception("Operator stack empty")
                if operators[-1]["type"] == "(":
                    raise Exception("Invalid brackets")
                raise Exception("Operator missing operand: " + str(operators[-1]))
            else:
                raise Exception("Expecting variable, constant, or (")
        else:
            if isBinaryOperator(t) or t["type"] == "$":

                while (True):
                    if len(operators) == 0 or operators[-1]["type"] == "(":
                        break
                    # print(t)
                    if priority(operators[-1]) <= priority(t):
                        break

                    operator = operators.pop(len(operators) - 1)
                    right = operands.pop(len(operands) - 1)
                    left = operands.pop(len(operands) - 1)

                    addOperand(createOperatorNode(left, operator, right), operands, operators)

                operators.append(t)
                needOperand = True
                if t["type"] == "$":
                    break

            elif t["type"] == ")":
                while (True):
                    if len(operators) == 0:
                        raise Exception(") doesn't match any (")
                    cur_op = operators.pop(len(operators) - 1)

                    if cur_op["type"] == "(":
                        break
                    elif cur_op["type"] == "!":
                        raise Exception("Nothing to negate")

                    right = operands.pop(len(operands) - 1)
                    left = operands.pop(len(operands) - 1)
                    addOperand(createOperatorNode(left, cur_op, right), operands, operators)
                exp = operands.pop(len(operands) - 1)
                addOperand(exp, operands, operators)
            else:
                raise Exception("expecting ) or binary operator at " + str(t["start"]))

    assert (len(operators) != 0)
    assert (operators.pop(len(operators) - 1)["type"] == "$")

    return {"ast": operands.pop(len(operands) - 1), "variables": scanResult["variables"]}


def next_assign(assign):
    flip = len(assign) - 1
    while (flip >= 0 and assign[flip]):
        flip -= 1
    if flip == -1:
        return False
    assign[flip] = True
    for i in range(flip + 1, len(assign)):
        assign[i] = False

    return True

def union_variable_set(input_list):
    new_input_list = []
    scanned_variables_map = {input_str: scan(input_str)["variables"] for input_str in
                             input_list}  # [set(scan(i).variables) for i in input_list]
    union_var_set = set().union(*(scanned_variables_map.values()))
    for input_str in input_list:
        extra_vars = union_var_set.difference(set(scanned_variables_map[input_str]))
        if not extra_vars:
            new_input_list.append(input_str)
        else:
            new_input_list.append(
                "(" + input_str + ")| ((" + input_str + ") &" + " & ".join([v + " " for v in extra_vars]) + ")")

    return new_input_list

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

class expressionHandler:
    def __init__(self, s):
        self.user_input = [replace_operators(s)]
        self.variables = []
        self.ans = [[]]
        new_input_list = union_variable_set(self.user_input)

        pr = parse(new_input_list[0])
        for v in pr["variables"]:
            self.variables.append(v)

        parse_res_list = [pr]

        num_vars = len(pr["variables"])

        for i in range(1, len(new_input_list)):
            p = parse(new_input_list[i])
            parse_res_list.append(p)

        assign = [False] * len(pr["variables"])
        # print(assign)
        # print(pr["variables"])
        # left side first
        while (True):
            new_row = []
            for x in assign:
                new_row.append(x)
            self.ans.append(new_row)
            if not next_assign(assign):
                break
            # print(assign)
        self.ans.pop(0)

        for p in parse_res_list:
            assign = [False] * len(pr["variables"])
            index = 0
            while (True):
                self.ans[index].append(p["ast"].evaluate(assign))
                index += 1
                if not next_assign(assign):
                    break


    def getTruthtable(self):
        return self.ans

    def getParameters(self):
        return self.variables