# Import necessary modules
import pygame
import random
from googletrans import Translator
from DNFGenerator import DNFGenerator
from logicGenerator import get_questions
from Integrated import list_questions
import random



# Set constants for window dimensions and colours
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (0, 0 , 64)
DARKER_BLUE = (0, 0, 32)
BLUE = (13, 27, 42)
LIGHT_BLUE = (173, 216, 230)
SKY_BLUE = (135, 206, 235)
ROYAL_BLUE = (65, 105, 225)
NAVY_BLUE = (30, 144, 255)

# List of words that are used in the program
ENGLISH = ["DNF Expressions", "START", "ACCESSIBILITY", "DNF EG is a learning tool designed to enhance your logic skills by generating",
           "random problem sets and giving you the opprtunity to test yourself.", "Validity Exercises", "Satisfiability Exercises",
           "Truth Table Exercises", "TRUE", "FALSE", "Correct!", "Incorrect!", "Select Language", "GO BACK"]

# Define radius for buttons and their center positions
RADIUS = 45
theme1_center = pygame.math.Vector2(1050, 550)
theme2_center = pygame.math.Vector2(1050, 650)

# Set up questions and their corresponding answers
random_question = ""
questions = ["10 + 5 = 15", "15 + 6 = 20", "22 - 12 = 8", "1 + 23 = 24", "5 - 0 = 5", "21 - 9 = 100"]
question_answers = [True, False, False, True, True, False]
questions1 = ["10 - 5 = 5", "135 - 6 = 20", "22 - 101 = 8", "1 - 3 = -2", "51 - 1 = 50", "210 - 9 = 190"]
question1_answers = [True, False, False, True, True, False]
questions2 = ["5 - 5 = 0", "5 = 1", "100 - 10 = 80", "1 - 3 = -200", "511 - 1 = 510", "2 - 9 = -7"]
question2_answers = [True, False, False, False, True, True]

translator = Translator()

def setup(CURRENT_LANGUAGE):
    # Loads all librariies in module pygame
    pygame.init()

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
    print(mouse_pos)
    if button.collidepoint(mouse_pos):
        return True
    else:
        return False

def is_mouse_over_button(mouse_pos, button_center):
    return (mouse_pos - button_center).length() <= RADIUS


def generate_question(questions):
    # Only included for testing. The Qs will be replaced by DNF generator/ same w answers
    random_question = random.choice(questions)
    print(random_question)
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
    window.blit(text, (WIDTH // 2 - (text.get_width() // 2), 50))
    pygame.display.update()
    pygame.time.wait(2000)

def incorrect_window(window, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT):
    font = pygame.font.SysFont(CURRENT_FONT, 50)
    text = font.render(CURRENT_LANGUAGE[11], True, COLOUR4) # "Incorrect!"
    window.blit(text, (WIDTH // 2 - (text.get_width() // 2), 50))
    pygame.display.update()
    pygame.time.wait(2000)

def setup_window2():
    # Set up the screen
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    # Set up the exercise buttons
    validity_button_rect = pygame.Rect(350, 200, 500, 100)
    satisfiability_button_rect = pygame.Rect(350, 400, 500, 100)
    truthtables_button_rect = pygame.Rect(350, 600, 500, 100)

    return window, validity_button_rect, satisfiability_button_rect, truthtables_button_rect, False, False, False

def draw_window2(window, validity_button_rect, satisfiability_button_rect, truthtables_button_rect, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT):
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

    pygame.draw.rect(window, validity_button_colour, validity_button_rect) # Validity Exercises
    pygame.draw.rect(window, satisfiability_button_colour, satisfiability_button_rect) # Satisfiability Exercises
    pygame.draw.rect(window, truthtables_button_colour, truthtables_button_rect) # Truth Table Exercises

    font = pygame.font.SysFont(CURRENT_FONT, 30)
    text = font.render(CURRENT_LANGUAGE[5], True, COLOUR4) # "Validity Exercises"
    window.blit(text, (validity_button_rect.centerx - text.get_width() // 2, validity_button_rect.centery - text.get_height() // 2))

    text = font.render(CURRENT_LANGUAGE[6], True, COLOUR4) # "Satisfiability Exercises"
    window.blit(text, (satisfiability_button_rect.centerx - text.get_width() // 2, satisfiability_button_rect.centery - text.get_height() // 2))

    text = font.render(CURRENT_LANGUAGE[7], True, COLOUR4) # "Truth Table Exercises"
    window.blit(text, (truthtables_button_rect.centerx - text.get_width() // 2, truthtables_button_rect.centery - text.get_height() // 2))

    # Update the screen
    pygame.display.update()


def setup_window3():
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    option1 = pygame.Rect(400, 400, 400, 100)  # True
    option2 = pygame.Rect(400, 600, 400, 100)  # False

    return window, option1, option2, False, False

def draw_window3(window, option1, option2, questions, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT): #might add OPTION 3 # VALIDITY
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

    questions = list_questions()
    print(questions)

    random_question = DNFGenerator(random.choice(questions))
    text = font.render(random_question.expression, True, COLOUR4)
    text_rect = text.get_rect(center=(pygame.Rect(300, 200, 600, 100)).center)
    window.blit(text, (text_rect))

    pygame.display.update()

def setup_window4():
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    option3 = pygame.Rect(400, 400, 400, 100)  # True
    option4 = pygame.Rect(400, 600, 400, 100)  # False

    return window, option3, option4, False, False

def setup_window5():
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    option5 = pygame.Rect(700, 150, 300, 100)  # True
    option6 = pygame.Rect(700, 350, 300, 100)  # False

    return window, option5, option6, False, False

def draw_window5(window, option1, option2, questions, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT): #might add OPTION 3 # VALIDITY
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


    pygame.draw.rect(window, (option1_colour), option1) # True button
    pygame.draw.rect(window, (option2_colour), option2) # False button

    pygame.draw.rect(window, (COLOUR2), (200, 200, 300, 400)) # Question box

    font = pygame.font.SysFont(CURRENT_FONT, 30)
    text = font.render(CURRENT_LANGUAGE[8].upper(), True, COLOUR4) # "True"
    text_rect = text.get_rect(center=option1.center)
    window.blit(text, text_rect)

    text = font.render(CURRENT_LANGUAGE[9].upper(), True, COLOUR4) # "False"
    text_rect = text.get_rect(center=option2.center)
    window.blit(text, text_rect)

    text = font.render(random_question, True, COLOUR4)
    window.blit(text, (250, 400))

    pygame.display.update()

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

def translate_tool(language, ENGLISH):
    CURRENT_LANGUAGE = []
    for i in range(len(ENGLISH)):
        text = ENGLISH[i]
        print(i)
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
                    print("access clicked")
                elif is_mouse_over_button(pygame.mouse.get_pos(), theme1_center):
                    print("DARK_THEME")
                    COLOUR1 = BLUE
                    COLOUR2 = DARKER_BLUE
                    COLOUR3 = DARK_BLUE
                    COLOUR4 = LIGHT_BLUE

                elif is_mouse_over_button(pygame.mouse.get_pos(), theme2_center):
                    print("LIGHT_THEME")
                    COLOUR1 = SKY_BLUE
                    COLOUR2 = ROYAL_BLUE
                    COLOUR3 = NAVY_BLUE
                    COLOUR4 = BLACK


        draw_window(window, start_button_rect, accessibility_button_rect, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)

        if start_clicked:
            window2, validity_button_rect, satisfiability_button_rect, truthtables_button_rect, validity_clicked, \
            satisfiability_clicked, truthtables_clicked = setup_window2()
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


                draw_window2(window2, validity_button_rect, satisfiability_button_rect, truthtables_button_rect, COLOUR1, COLOUR2, COLOUR3, COLOUR4,
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
                                result, random_question = check_answer(window, answer, question1_answers, questions1, COLOUR4,
                                                                       CURRENT_LANGUAGE, CURRENT_FONT)
                                if result:
                                    correct_answers = correct_answers + 1
                                    print(correct_answers)


                        draw_window3(window, option3, option4, questions1, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)
                elif truthtables_clicked:
                    window, option5, option6, option5_clicked, option6_clicked = setup_window5()
                    print("SETUP tables")
                    running5 = True
                    while running5:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running5 = False
                                pygame.quit()
                            elif event.type == pygame.MOUSEBUTTONDOWN:
                                if check_button_click(option5):
                                    answer = True
                                elif check_button_click(option6):
                                    answer = False
                                result, random_question = check_answer(window, answer, question2_answers, questions2,
                                                                       COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)
                                if result:
                                    correct_answers = correct_answers + 1

                        draw_window5(window, option5, option6, questions2, COLOUR1, COLOUR2, COLOUR3, COLOUR4, CURRENT_LANGUAGE, CURRENT_FONT)

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
