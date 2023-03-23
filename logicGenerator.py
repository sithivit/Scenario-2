import openai
from DNFGenerator import DNFGenerator
import random

def get_questions(max_variable):
    openai.api_key = "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"

    messages = [
        {"role": "system",
         "content": f"Can you create 5 random solvable propositional logic expressions with each max {max_variable} variables using \/ for or /\ for and -> for imply ~ for not <=> for equivalent syntax and using A B C ... as variable"}
    ]

    chat = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )

    reply = chat.choices[0].message.content

    messages.append({"role": "assistant", "content": reply})
    return reply, messages

def list_questions():
    done = False
    result = []
    while not done:
        questions, messages = get_questions(5)
        temp = [i for i in questions.split('\n') if i != '']
        for i in temp:
            result.append(i.split('.')[1])
        done = True
    return result

def replace_character(string, old, new):
    copy = ""
    for i in string:
        if i == old:
            copy += new
        else:
            copy += i
    return copy

def get_answer(question):
    replace_operator = zip(['!', '|', '&', '=>', '<=>'], ['not ', 'or', 'and', 'or', 'or'])
    DNF = DNFGenerator(question)
    num_parameters = len(DNF.parameters)
    expression = DNF.valid_expression[0]
    for j, k in replace_operator:
        expression = expression.replace(j, k)

    print(expression)
    parameters = DNF.parameters
    possible_conditions = [bin(i).replace("0b", "") for i in range(2**num_parameters)]
    possible_conditions = [(num_parameters-len(i))*'0' + i for i in possible_conditions]
    print(possible_conditions)
    for i in possible_conditions:
        condition = [*i]
        variable_condition = zip(parameters, condition)
        temp = expression
        for i, j in variable_condition:
            temp = replace_character(temp, i, j)
        print(temp)
        print(eval(temp))



questions = list_questions()
get_answer(random.choice(questions))
