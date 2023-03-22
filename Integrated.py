from TruthTable import expressionHandler
from DNFGenerator import DNFGenerator
from logicGenerator import get_questions


def list_questions():
    done = False
    while not done:
        try:
            questions, messages = get_questions(5)
            result = []
            temp = [i for i in questions.split('\n') if i != '']
            for i in temp:
                try:
                    result.append(i.split('.')[1])
                except:
                    pass
            return result
        except:
            done = True


