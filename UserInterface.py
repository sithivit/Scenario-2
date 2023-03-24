# Import necessary modules
import pygame
import random
from googletrans import Translator
from logicGenerator import get_answer_satisfy, get_answer_validation, get_table


# Set constants for window dimensions and colours
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0, 64)
DARKER_BLUE = (0, 0, 32)
BLUE = (13, 27, 42)
LIGHT_BLUE = (173, 216, 230)
SKY_BLUE = (135, 206, 235)
ROYAL_BLUE = (65, 105, 225)
NAVY_BLUE = (30, 144, 255)

# List of words that are used in the program
ENGLISH = ["DNF Expressions", "START", "ACCESSIBILITY", "DNF EG is a learning tool designed to enhance your logic skills by generating",
           "random problem sets and giving you the opprtunity to test yourself.", "Validity Exercises", "Satisfiability Exercises",
           "Truth Table Exercises", "YES", "NO", "Correct!", "Incorrect!", "Select Language", "GO BACK", "Is the expression valid?", "Is the expression satisfiable?",
           "Select an option to fill in the missing output column", "Add your question", "Confirm"]

# Define radius for buttons and their center positions
RADIUS = 45
theme1_center = pygame.math.Vector2(1050, 550)
theme2_center = pygame.math.Vector2(1050, 650)

# Set up questions and their corresponding answers

questions2 = ["5 - 5 = 0", "5 = 1", "100 - 10 = 80", "1 - 3 = -200", "511 - 1 = 510", "2 - 9 = -7"]
question2_answers = [True, False, False, False, True, True]

translator = Translator()

def setup(CURRENT_LANGUAGE):
    # Loads all librariies in module pygame
    pygame.init()
    pygame.mouse.set_cursor(*pygame.cursors.arrow)
    # Set up the screen
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption(CURRENT_LANGUAGE[0])

    start_button_rect = pygame.Rect(400, 400, 400, 100)#start button
    accessibility_button_rect = pygame.Rect(400, 600, 400, 100)#accessibility button

    return window, start_button_rect, accessibility_button_rect, False, False


def draw_window(window, start_button_rect, accessibility_button_rect, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT): #create new colours like light: dark: neutral: background:
    # Clear the screen
    window.fill(COLOUR1)

    # Change the colour of the button if the mouse is hovering it
    mouse_pos = pygame.mouse.get_pos()
    if start_button_rect.collidepoint(mouse_pos):
        start_button_colour = COLOUR3
    else:
        start_button_colour = COLOUR2
    if accessibility_button_rect.collidepoint(mouse_pos):
        accessibility_button_colour = COLOUR3
    else:
        accessibility_button_colour = COLOUR2


    # START button
    pygame.draw.rect(window, (start_button_colour), start_button_rect)
    # ACCESSIBILITY button
    pygame.draw.rect(window, (accessibility_button_colour), (accessibility_button_rect))
    # Themes options
    pygame.draw.circle(window, BLACK, (1050, 550), RADIUS) #DARK theme
    pygame.draw.circle(window, WHITE, (1050, 650), RADIUS) #LIGHT theme

    # Add text
    font = pygame.font.SysFont(CURRENT_FONT, 30)
    #
    text = font.render(CURRENT_LANGUAGE[1], True, COLOUR4) # Text for "START"
    text_rect = text.get_rect(center=start_button_rect.center)
    window.blit(text, text_rect)

    text = font.render(CURRENT_LANGUAGE[2], True, COLOUR4) # "ACCESSIBILITY"
    text_rect = text.get_rect(center=accessibility_button_rect.center)
    window.blit(text, text_rect)

    # Add text
    font = pygame.font.SysFont(CURRENT_FONT, 60)
    text = font.render(CURRENT_LANGUAGE[0], True, COLOUR4) # "DNF Expressions"
    text_rect = text.get_rect(centerx=WIDTH / 2, y=100)
    window.blit(text, text_rect)

    font = pygame.font.SysFont(CURRENT_FONT, 20)
    text = font.render(CURRENT_LANGUAGE[3], True, COLOUR4) # "DNF EG is a learning tool designed to enhance your logic skills by generating"
    text_rect = text.get_rect(centerx=WIDTH / 2, y=200)
    window.blit(text, text_rect)

    text = font.render(CURRENT_LANGUAGE[4], True, COLOUR4) # "random problem sets and giving you the opprtunity to test yourself."
    text_rect = text.get_rect(centerx=WIDTH / 2, y=225)
    window.blit(text, text_rect)

    # update the screen
    pygame.display.update()


def check_button_click(button):
    # Checks if the button has been clicked
    mouse_pos = pygame.mouse.get_pos()
    if button.collidepoint(mouse_pos):
        return True
    else:
        return False

def retrieve_from_file():
    with open('expressions_set.txt', 'r') as file:
        lines = file.readlines()
        expressions = []
        for line in lines:
            expressions.append(line.strip())  # strip() removes the trailing newline character
    file.close()
    return expressions

def add_to_file(expression):
    with open('expressions_set.txt', 'a') as file:
        file.write('\n' + expression)
    file.close()


random_question = ""
questions = retrieve_from_file()
question_answers = [get_answer_validation(i) for i in questions]
question1_answers = [get_answer_satisfy(j) for j in questions]

def is_mouse_over_button(mouse_pos, button_center):
    return (mouse_pos - button_center).length() <= RADIUS


def generate_question(questions):
    random_question = random.choice(questions)
    return random_question

def check_answer(window, answer, answers, questions, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT):
    # Check if the answer is correct
    global random_question
    question_index = questions.index(random_question)
    question_answer = answers[question_index]
    if answer == question_answer:
        correct_window(window, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)
        random_question = ""  # Reset the question
        return True, random_question
    else:
        incorrect_window(window, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)

        return False, random_question

def correct_window(window, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT):
    font = pygame.font.SysFont(CURRENT_FONT, 50)
    text = font.render(CURRENT_LANGUAGE[10], True, COLOUR4) # "Correct!"
    window.blit(text, (WIDTH // 2 - (text.get_width() // 2), 0))
    pygame.display.update()
    pygame.time.wait(2000)

def incorrect_window(window, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT):
    font = pygame.font.SysFont(CURRENT_FONT, 50)
    text = font.render(CURRENT_LANGUAGE[11], True, COLOUR4) # "Incorrect!"
    window.blit(text, (WIDTH // 2 - (text.get_width() // 2), 0))
    pygame.display.update()
    pygame.time.wait(2000)

def setup_window2():
    # Set up the screen
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    # Set up the exercise buttons
    validity_button_rect = pygame.Rect(350, 100, 500, 100)
    satisfiability_button_rect = pygame.Rect(350, 300, 500, 100)
    truthtables_button_rect = pygame.Rect(350, 500, 500, 100)
    add_a_question_rect = pygame.Rect(350, 700, 500, 100)

    return window, validity_button_rect, satisfiability_button_rect, truthtables_button_rect, add_a_question_rect, False, False, False, False

def draw_window2(window, validity_button_rect, satisfiability_button_rect, truthtables_button_rect, add_a_question_rect, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT):
    window.fill(COLOUR1)

    # Check if the mouse is hovering over any button
    mouse_pos = pygame.mouse.get_pos()
    if validity_button_rect.collidepoint(mouse_pos):
        validity_button_colour = COLOUR3
    else:
        validity_button_colour = COLOUR2

    if satisfiability_button_rect.collidepoint(mouse_pos):
        satisfiability_button_colour = COLOUR3
    else:
        satisfiability_button_colour = COLOUR2

    if truthtables_button_rect.collidepoint(mouse_pos):
        truthtables_button_colour = COLOUR3
    else:
        truthtables_button_colour = COLOUR2

    if add_a_question_rect.collidepoint(mouse_pos):
        add_a_question_button_colour = COLOUR3
    else:
        add_a_question_button_colour = COLOUR2

    pygame.draw.rect(window, validity_button_colour, validity_button_rect) # Validity Exercises
    pygame.draw.rect(window, satisfiability_button_colour, satisfiability_button_rect) # Satisfiability Exercises
    pygame.draw.rect(window, truthtables_button_colour, truthtables_button_rect) # Truth Table Exercises
    pygame.draw.rect(window, add_a_question_button_colour, add_a_question_rect)


    font = pygame.font.SysFont(CURRENT_FONT, 30)
    text = font.render(CURRENT_LANGUAGE[5], True, COLOUR4) # "Validity Exercises"
    window.blit(text, (validity_button_rect.centerx - text.get_width() // 2, validity_button_rect.centery - text.get_height() // 2))

    text = font.render(CURRENT_LANGUAGE[6], True, COLOUR4) # "Satisfiability Exercises"
    window.blit(text, (satisfiability_button_rect.centerx - text.get_width() // 2, satisfiability_button_rect.centery - text.get_height() // 2))

    text = font.render(CURRENT_LANGUAGE[7], True, COLOUR4) # "Truth Table Exercises"
    window.blit(text, (truthtables_button_rect.centerx - text.get_width() // 2, truthtables_button_rect.centery - text.get_height() // 2))

    text = font.render(CURRENT_LANGUAGE[17], True, COLOUR4)
    window.blit(text, (add_a_question_rect.centerx - text.get_width() // 2, add_a_question_rect.centery - text.get_height() // 2))

    # Update the screen
    pygame.display.update()


def setup_window3():
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    option1 = pygame.Rect(400, 400, 400, 100)  # True
    option2 = pygame.Rect(400, 600, 400, 100)  # False

    return window, option1, option2, False, False

def draw_window3(window, option1, option2, questions, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT):
    window.fill(COLOUR1)

    # Check if the mouse is hovering over any button
    mouse_pos = pygame.mouse.get_pos()
    if option1.collidepoint(mouse_pos):
        option1_colour = COLOUR3
    else:
        option1_colour = COLOUR2

    if option2.collidepoint(mouse_pos):
        option2_colour = COLOUR3
    else:
        option2_colour = COLOUR2


    global random_question
    if not random_question:
        random_question = generate_question(questions)


    pygame.draw.rect(window, (option1_colour), option1) # True
    pygame.draw.rect(window, (option2_colour), option2) # False
    pygame.draw.rect(window, (COLOUR2), (300, 200, 600, 100)) # Question box

    font = pygame.font.SysFont(CURRENT_FONT, 30)
    text = font.render(CURRENT_LANGUAGE[8].upper(), True, COLOUR4) # "True"
    text_rect = text.get_rect(center=option1.center)
    window.blit(text, text_rect)

    text = font.render(CURRENT_LANGUAGE[9].upper(), True, COLOUR4)  # "False"
    text_rect = text.get_rect(center=option2.center)
    window.blit(text, text_rect)

    text = font.render(random_question, True, COLOUR4)
    text_rect = text.get_rect(center=(pygame.Rect(300, 200, 600, 100)).center)
    window.blit(text, (text_rect))

    text = font.render(CURRENT_LANGUAGE[14], True, COLOUR4)
    text_rect = text.get_rect(centerx=WIDTH / 2, y=125)
    window.blit(text, text_rect)

    pygame.display.update()

def setup_window4():
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    option3 = pygame.Rect(400, 400, 400, 100)  # True
    option4 = pygame.Rect(400, 600, 400, 100)  # False

    return window, option3, option4, False, False

def setup_window5(questions):
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    global random_question

    #if not random_question:
    random_question = generate_question(questions)

    table, no_of_variables, table_answers = get_table(random_question)
    wrong_answers = generate_wrong_answers(no_of_variables)
    option5 = pygame.Rect(700, 200, 90, 2**no_of_variables * 50 + 50)  # True
    option6 = pygame.Rect(800, 200, 90, 2**no_of_variables * 50 + 50)  # False

    return window, option5, option6, False, False, random_question, wrong_answers

def draw_window5(window, correct_button, wrong_button, random_question, wrong_answers, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT):
    window.fill(COLOUR1)

    # Check if the mouse is hovering over any button
    mouse_pos = pygame.mouse.get_pos()
    if correct_button.collidepoint(mouse_pos):
        correct_button_colour = COLOUR3
    else:
        correct_button_colour = COLOUR2

    if wrong_button.collidepoint(mouse_pos):
        wrong_button_colour = COLOUR3
    else:
        wrong_button_colour = COLOUR2

    font = pygame.font.SysFont(CURRENT_FONT, 30)

    text = font.render(CURRENT_LANGUAGE[16], True, COLOUR4)
    text_rect = text.get_rect(centerx=WIDTH / 2, y=65)
    window.blit(text, text_rect)


    table, no_of_variables, table_answers = get_table(random_question)
    for i in range(len(table)):
        for j in range(len(table[i])):
            text = font.render((table[i][j]), True, COLOUR4)
            window.blit(text, (100 + j * 100, 200 + i * 50))

    pygame.draw.rect(window, (correct_button_colour), correct_button) # True button
    pygame.draw.rect(window, (wrong_button_colour), wrong_button) # False button

    for i in range(len(table_answers)):

        text = font.render((str(table_answers[i])), True, COLOUR4)
        text_rect = text.get_rect(centerx=(correct_button.centerx), y=(250 + i * 50))
        window.blit(text, text_rect)

    for j in range(len(wrong_answers)):
        text = font.render((str(wrong_answers[j])), True, COLOUR4)
        text_rect = text.get_rect(centerx=(wrong_button.centerx), y=(250 + j * 50))
        window.blit(text, text_rect)


    pygame.display.update()


def create_buttons(button1, button2):
    random_assignment = random.choice([0,1])
    if random_assignment == 0:
        correct_button = button1
        wrong_button = button2
    else:
        correct_button = button2
        wrong_button = button1
    return correct_button, wrong_button


def setup_window6():

    window = pygame.display.set_mode((WIDTH, HEIGHT))

    language1 = pygame.Rect(350, 200, 500, 90)  # English
    language2 = pygame.Rect(350, 300, 500, 90) # Turkish
    language3 = pygame.Rect(350, 400, 500, 90) # Chinese
    language4 = pygame.Rect(350, 500, 500, 90) # Thai
    language5 = pygame.Rect(350, 600, 500, 90) # Russian
    go_back = pygame.Rect(450, 700, 300, 90)

    return window, language1, language2, language3, language4, language5, go_back

def draw_window6(window, language1, language2, language3, language4, language5, go_back, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT): #might add OPTION 3 # VALIDITY
    window.fill(COLOUR1)

    mouse_pos = pygame.mouse.get_pos()
    if language1.collidepoint(mouse_pos):
        language1_colour = COLOUR3
    else:
        language1_colour = COLOUR2

    if language2.collidepoint(mouse_pos):
        language2_colour = COLOUR3
    else:
        language2_colour = COLOUR2

    if language3.collidepoint(mouse_pos):
        language3_colour = COLOUR3
    else:
        language3_colour = COLOUR2

    if language4.collidepoint(mouse_pos):
        language4_colour = COLOUR3
    else:
        language4_colour = COLOUR2

    if language5.collidepoint(mouse_pos):
        language5_colour = COLOUR3
    else:
        language5_colour = COLOUR2

    if go_back.collidepoint(mouse_pos):
        go_back_colour = COLOUR3
    else:
        go_back_colour = COLOUR2


    pygame.draw.rect(window, (language1_colour), language1) #English
    pygame.draw.rect(window, (language2_colour), language2) #Turkish
    pygame.draw.rect(window, (language3_colour), language3) #Chinese
    pygame.draw.rect(window, (language4_colour), language4) #Thai
    pygame.draw.rect(window, (language5_colour), language5) #Russian
    pygame.draw.rect(window, (go_back_colour), go_back) #Go back option


    font = pygame.font.SysFont(CURRENT_FONT, 50)
    text = font.render(CURRENT_LANGUAGE[12], True, COLOUR4)
    text_x = (WIDTH - text.get_width()) // 2
    window.blit(text, (text_x, 100))

    font = pygame.font.SysFont(CURRENT_FONT, 30)

    text = font.render("ENGLISH", True, COLOUR4)
    text_rect = text.get_rect(center=language1.center)
    window.blit(text, text_rect)

    text = font.render("TURKISH", True, COLOUR4)
    text_rect = text.get_rect(center=language2.center)
    window.blit(text, text_rect)

    text = font.render("CHINESE", True, COLOUR4)
    text_rect = text.get_rect(center=language3.center)
    window.blit(text, text_rect)

    text = font.render("THAI", True, COLOUR4)
    text_rect = text.get_rect(center=language4.center)
    window.blit(text, text_rect)

    text = font.render("RUSSIAN", True, COLOUR4)
    text_rect = text.get_rect(center=language5.center)
    window.blit(text, text_rect)

    text = font.render(CURRENT_LANGUAGE[13], True, COLOUR4)
    text_rect = text.get_rect(center= go_back.center)
    window.blit(text, text_rect)

    pygame.display.update()

def setup_window7():

    window = pygame.display.set_mode((WIDTH, HEIGHT))

    add_a_question = pygame.Rect(350, 200, 500, 90)  # English
    A_button = pygame.Rect(125, 350, 50, 50)
    B_button = pygame.Rect(225, 350, 50, 50)
    C_button = pygame.Rect(325, 350, 50, 50)
    not_button = pygame.Rect(425, 350, 50, 50)
    and_button = pygame.Rect(525, 350, 50, 50)
    or_button = pygame.Rect(625, 350, 50, 50)
    implication_button = pygame.Rect(725, 350, 50, 50)
    bracket1_button = pygame.Rect(825, 350, 50, 50)
    bracket2_button = pygame.Rect(925, 350, 50, 50)
    remove_button = pygame.Rect(1025, 350, 50, 50)
    confirm_button = pygame.Rect(450, 600, 300, 90)
    go_back = pygame.Rect(450, 700, 300, 90)

    return window, add_a_question, A_button, B_button, C_button, not_button, and_button, or_button, implication_button, bracket1_button, \
           bracket2_button, remove_button, confirm_button, go_back

def draw_window7(window, add_a_question, expression, A_button, B_button, C_button, not_button, and_button, or_button, implication_button, bracket1_button,
                 bracket2_button, remove_button, confirm_button, go_back, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT):
    window.fill(COLOUR1)

    mouse_pos = pygame.mouse.get_pos()

    add_a_question_colour = check_if_hovering(add_a_question, mouse_pos, COLOUR2, COLOUR3)
    A_button_colour = check_if_hovering(A_button, mouse_pos, COLOUR2, COLOUR3)
    B_button_colour = check_if_hovering(B_button, mouse_pos, COLOUR2, COLOUR3)
    C_button_colour = check_if_hovering(C_button, mouse_pos, COLOUR2, COLOUR3)
    not_button_colour = check_if_hovering(not_button, mouse_pos, COLOUR2, COLOUR3)
    and_button_colour = check_if_hovering(and_button, mouse_pos, COLOUR2, COLOUR3)
    or_button_colour = check_if_hovering(or_button, mouse_pos, COLOUR2, COLOUR3)
    implication_button_colour = check_if_hovering(implication_button, mouse_pos, COLOUR2, COLOUR3)
    go_back_colour = check_if_hovering(go_back, mouse_pos, COLOUR2, COLOUR3)
    bracket1_button_colour = check_if_hovering(bracket1_button, mouse_pos, COLOUR2, COLOUR3)
    bracket2_button_colour = check_if_hovering(bracket2_button, mouse_pos, COLOUR2, COLOUR3)
    remove_button_colour = check_if_hovering(remove_button, mouse_pos, COLOUR2, COLOUR3)
    confirm_button_colour = check_if_hovering(confirm_button, mouse_pos, COLOUR2, COLOUR3)


    pygame.draw.rect(window, (add_a_question_colour), add_a_question)
    pygame.draw.rect(window, (A_button_colour), A_button)
    pygame.draw.rect(window, (B_button_colour), B_button)
    pygame.draw.rect(window, (C_button_colour), C_button)
    pygame.draw.rect(window, (not_button_colour), not_button)
    pygame.draw.rect(window, (and_button_colour), and_button)
    pygame.draw.rect(window, (or_button_colour), or_button)
    pygame.draw.rect(window, (implication_button_colour), implication_button)
    pygame.draw.rect(window, (bracket1_button_colour), bracket1_button)
    pygame.draw.rect(window, (bracket2_button_colour), bracket2_button)
    pygame.draw.rect(window, (remove_button_colour), remove_button)
    pygame.draw.rect(window, (confirm_button_colour), confirm_button)
    pygame.draw.rect(window, (go_back_colour), go_back) #Go back option

    font = pygame.font.SysFont(CURRENT_FONT, 50)
    text = font.render("Add your question", True, COLOUR4)
    text_x = (WIDTH - text.get_width()) // 2
    window.blit(text, (text_x, 100))

    font = pygame.font.SysFont(CURRENT_FONT, 30)

    text = font.render("A", True, COLOUR4)
    text_rect = text.get_rect(center= A_button.center)
    window.blit(text, text_rect)

    text = font.render("B", True, COLOUR4)
    text_rect = text.get_rect(center= B_button.center)
    window.blit(text, text_rect)

    text = font.render("C", True, COLOUR4)
    text_rect = text.get_rect(center= C_button.center)
    window.blit(text, text_rect)

    text = font.render("~", True, COLOUR4)
    text_rect = text.get_rect(center= not_button.center)
    window.blit(text, text_rect)

    text = font.render("/\\", True, COLOUR4)
    text_rect = text.get_rect(center= and_button.center)
    window.blit(text, text_rect)

    text = font.render("\/", True, COLOUR4)
    text_rect = text.get_rect(center= or_button.center)
    window.blit(text, text_rect)

    text = font.render("->", True, COLOUR4)
    text_rect = text.get_rect(center= implication_button.center)
    window.blit(text, text_rect)

    text = font.render("(", True, COLOUR4)
    text_rect = text.get_rect(center= bracket1_button.center)
    window.blit(text, text_rect)

    text = font.render(")", True, COLOUR4)
    text_rect = text.get_rect(center= bracket2_button.center)
    window.blit(text, text_rect)

    text = font.render("<-", True, COLOUR4)
    text_rect = text.get_rect(center= remove_button.center)
    window.blit(text, text_rect)

    text = font.render(CURRENT_LANGUAGE[18], True, COLOUR4)
    text_rect = text.get_rect(center= confirm_button.center)
    window.blit(text, text_rect)

    text = font.render(CURRENT_LANGUAGE[13], True, COLOUR4)
    text_rect = text.get_rect(center= go_back.center)
    window.blit(text, text_rect)

    text = font.render(expression, True, COLOUR4)
    text_rect = text.get_rect(center= add_a_question.center)
    window.blit(text, text_rect)

    pygame.display.update()

def check_if_hovering(button, mouse_pos, COLOUR2, COLOUR3):
    if button.collidepoint(mouse_pos):
        button_colour = COLOUR3
    else:
        button_colour = COLOUR2
    return button_colour


def generate_wrong_answers(no_of_variables):
    wrong_answers = []
    for a in range(2**no_of_variables):
        wrong_answers.append(random.choice([0, 1]))
    return wrong_answers

def translate_tool(language, ENGLISH):
    CURRENT_LANGUAGE = []
    for i in range(len(ENGLISH)):
        text = ENGLISH[i]
        CURRENT_LANGUAGE.append(translator.translate(text, dest= language).text)

    return CURRENT_LANGUAGE



def main():
    CURRENT_FONT = "Arial"
    CURRENT_LANGUAGE = ENGLISH
    COLOUR1 = BLUE
    COLOUR2 = DARKER_BLUE
    COLOUR3 = DARK_BLUE
    COLOUR4 = LIGHT_BLUE

    window, start_button_rect, accessibility_button_rect, start_clicked, accessibility_clicked = setup(CURRENT_LANGUAGE)
    correct_answers = 0
    # Set up the game loop

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if check_button_click(start_button_rect):
                    start_clicked = True
                elif check_button_click(accessibility_button_rect):
                    accessibility_clicked = True
                elif is_mouse_over_button(pygame.mouse.get_pos(), theme1_center):
                    COLOUR1 = BLUE
                    COLOUR2 = DARKER_BLUE
                    COLOUR3 = DARK_BLUE
                    COLOUR4 = LIGHT_BLUE
                elif is_mouse_over_button(pygame.mouse.get_pos(), theme2_center):
                    COLOUR1 = SKY_BLUE
                    COLOUR2 = ROYAL_BLUE
                    COLOUR3 = NAVY_BLUE
                    COLOUR4 = BLACK


        draw_window(window, start_button_rect, accessibility_button_rect, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)

        if start_clicked:
            window2, validity_button_rect, satisfiability_button_rect, truthtables_button_rect, add_a_question_rect, validity_clicked, \
            satisfiability_clicked, truthtables_clicked, add_a_question_clicked = setup_window2()
            running2 = True
            while running2:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running2 = False
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if check_button_click(validity_button_rect):
                            validity_clicked = True
                        elif check_button_click(satisfiability_button_rect):
                            satisfiability_clicked = True
                        elif check_button_click(truthtables_button_rect):
                            truthtables_clicked = True
                        elif check_button_click(add_a_question_rect):
                            add_a_question_clicked = True


                draw_window2(window2, validity_button_rect, satisfiability_button_rect, truthtables_button_rect, add_a_question_rect, COLOUR1, COLOUR2, COLOUR3, COLOUR4,
                             CURRENT_LANGUAGE, CURRENT_FONT)

                if validity_clicked:
                    window, option1, option2, option1_clicked, option2_clicked = setup_window3()
                    running3 = True
                    while running3:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running3 = False
                                pygame.quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if check_button_click(option1):
                                    answer = True
                                elif check_button_click(option2):
                                    answer = False
                                result, random_question = check_answer(window, answer, question_answers, questions, COLOUR4,
                                                                       CURRENT_LANGUAGE, CURRENT_FONT)
                                if result:
                                    correct_answers = correct_answers + 1
                                    print(correct_answers)

                        draw_window3(window, option1, option2, questions, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)

                elif satisfiability_clicked:
                    window, option3, option4, option3_clicked, option4_clicked = setup_window4()
                    running4 = True
                    CURRENT_LANGUAGE[14] = CURRENT_LANGUAGE[15]
                    while running4:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running4 = False
                                pygame.quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if check_button_click(option3):
                                    answer = True
                                elif check_button_click(option4):
                                    answer = False
                                result, random_question = check_answer(window, answer, question1_answers, questions, COLOUR4,
                                                                       CURRENT_LANGUAGE, CURRENT_FONT)
                                if result:
                                    correct_answers = correct_answers + 1
                                    print(correct_answers)

                        draw_window3(window, option3, option4, questions, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)
                elif truthtables_clicked:
                    window, option5, option6, option5_clicked, option6_clicked, random_question, wrong_answers = setup_window5(questions)
                    running5 = True
                    correct_button, wrong_button = create_buttons(option5, option6)
                    while running5:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running5 = False
                                pygame.quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if check_button_click(correct_button):
                                    correct_window(window, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)
                                    #window, option5, option6, option5_clicked, option6_clicked, random_question, wrong_answers = setup_window5(questions)
                                elif check_button_click(wrong_button):
                                    answer = False
                                    incorrect_window(window, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)
                                window, option5, option6, option5_clicked, option6_clicked, random_question, wrong_answers = setup_window5(questions)

                        draw_window5(window, correct_button, wrong_button, random_question, wrong_answers, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)

                elif add_a_question_clicked:
                    retrieve_from_file()
                    window, add_a_question, A_button, B_button, C_button, not_button, and_button, or_button, implication_button,\
                    bracket1_button, bracket2_button, remove_button, confirm_button, go_back = setup_window7()
                    new_expression = ""
                    running7 = True
                    while running7:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running7 = False
                                pygame.quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if check_button_click(A_button):
                                    new_expression += "A"
                                if check_button_click(B_button):
                                    new_expression += "B"
                                if check_button_click(C_button):
                                    new_expression += "C"
                                if check_button_click(not_button):
                                    new_expression += " ~ "
                                if check_button_click(and_button):
                                    new_expression += " /\\ "
                                if check_button_click(or_button):
                                    new_expression += " \/ "
                                if check_button_click(implication_button):
                                    new_expression += " -> "
                                if check_button_click(bracket1_button):
                                    new_expression += "( "
                                if check_button_click(bracket2_button):
                                    new_expression += " )"
                                if check_button_click(remove_button):
                                    new_expression = new_expression [:-1]
                                if check_button_click(confirm_button):
                                    add_to_file(new_expression)
                                    questions.append(new_expression)

                                if check_button_click(go_back):
                                    window2, validity_button_rect, satisfiability_button_rect, truthtables_button_rect, add_a_question_rect, validity_clicked, \
                                    satisfiability_clicked, truthtables_clicked, add_a_question_clicked = setup_window2()
                                    running7 = False

                        draw_window7(window, add_a_question, new_expression, A_button, B_button, C_button, not_button, and_button, or_button, implication_button,
                                     bracket1_button, bracket2_button, remove_button, confirm_button, go_back, COLOUR1, COLOUR2, COLOUR3, COLOUR4,
                                     CURRENT_LANGUAGE, CURRENT_FONT)


        elif accessibility_clicked:
            window, language1, language2, language3, language4, language5, go_back = setup_window6()
            running6 = True
            while running6:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running6 = False
                        pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if check_button_click(language1):
                            translate_to_language = "en"
                            CURRENT_LANGUAGE = translate_tool(translate_to_language, ENGLISH)

                        elif check_button_click(language2):
                            translate_to_language = "tr"
                            CURRENT_LANGUAGE = translate_tool(translate_to_language, ENGLISH)

                        elif check_button_click(language3):
                            CURRENT_FONT = "Microsoft JhengHei UI"
                            translate_to_language = "zh-CN"
                            CURRENT_LANGUAGE = translate_tool(translate_to_language, ENGLISH)

                        elif check_button_click(language4):
                            CURRENT_FONT = "Tahoma"
                            translate_to_language = "th"
                            CURRENT_LANGUAGE = translate_tool(translate_to_language, ENGLISH)

                        elif check_button_click(language5):
                            translate_to_language = "ru"
                            CURRENT_LANGUAGE = translate_tool(translate_to_language, ENGLISH)

                        elif check_button_click(go_back):

                            window, start_button_rect, accessibility_button_rect, start_clicked, accessibility_clicked = setup(CURRENT_LANGUAGE)
                            running6 = False
                draw_window6(window, language1, language2, language3, language4, language5, go_back, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)

    # Quit Pygame
    pygame.quit()

if __name__ == '__main__':
    main()
