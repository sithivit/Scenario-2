from TruthTable import expressionHandler
from DNFGenerator import DNFGenerator
from logicGenerator import get_questions


def list_questions():
    done = False
    result = []
    while not done:
        questions, messages = get_questions(5)
        temp = [i for i in questions.split('\n') if i != '']
        print("this is questions", questions)
        for i in temp:
            result.append(i.split('.')[1])
        done = True
    return result


