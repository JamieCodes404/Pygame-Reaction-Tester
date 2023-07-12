import pygame, sys
import time
import random  # so I can wait a random length of time

black = (0, 0, 0)  # rgb value for black
green = (0, 205, 0)  # rgb values for green background
red = (130, 0, 0)  # rgb values for red background
blue = (8, 96, 168)  # rgb values for blue
white = (255, 255, 255)  # rgb value for white

# set to monitor size / resolution (reduce SCREEN_HEIGHT if you want to make it windowed)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

X_CENTER = SCREEN_WIDTH / 2
Y_CENTER = SCREEN_HEIGHT / 2


def reaction_test(attempts):
    scores = []  # track time per attempt eg [120ms, 130ms 142ms]

    # Pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # set size of the screen and make a screen object

    large_font = pygame.font.SysFont('comicsansms', 60)
    medium_font = pygame.font.SysFont('comicsansms', 25)
    small_font = pygame.font.SysFont('comicsansms', 15)
    smallest_font = pygame.font.SysFont('comicsansms', 10)

    def change_bg(colour):
        screen.fill(colour)
        pygame.display.update()

    def display_text(font, text, colour, x, y):
        text = font.render(text, True, colour)
        text_rect = text.get_rect(center=(x, y))  # position text centered at x and y values
        screen.blit(text, text_rect)
        pygame.display.update()

    def left_click_pressed():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # give option to quit
                sys.exit()
            if pygame.mouse.get_pressed(3)[0]:
                return True
        return False

    def click_to_continue():  # the user needs to release the mouse and then click it down
        time.sleep(0.5)  # prevent mouse double clicks from skipping the continue page
        while not left_click_pressed():
            pass

        while left_click_pressed():
            pass

    def keep_red():
        change_bg(red)
        display_text(large_font, "Left-Click When The Background Turns Green", white, X_CENTER, Y_CENTER)

        delay = random.randint(1000, 7000) / 1000
        start_wait = time.time()

        # wait delay time before clicking
        while (time.time() - start_wait) < delay:
            if left_click_pressed() and (time.time() - start_wait > 0.5):  # if mouse clicked early also allow them to click the mouse in the first 0.5s in case of accidental clicks after clicking to continue
                change_bg(blue)
                display_text(large_font, 'Too Soon!', white, X_CENTER, Y_CENTER - 100)  # -100 to position 100 px upwards on the y-axis, so it is above the text below
                display_text(smallest_font, "Click to continue", white, X_CENTER, Y_CENTER)

                click_to_continue()
                keep_red()

    def display_average(lst):
        total = 0
        for value in lst:
            total += value

        average = round(total / len(scores))
        average_txt = "Your average reaction time was " + str(average) + " ms"

        # display average on the screen
        change_bg(white)
        display_text(medium_font, average_txt, black, X_CENTER, Y_CENTER-100)
        display_text(small_font, "click to exit", black, X_CENTER, Y_CENTER)


    # MAIN GAME
    running = True
    while running:
        for i in range(attempts):
            keep_red()

            change_bg(green)
            display_text(large_font, "Click!", white, X_CENTER, Y_CENTER)

            start_time = time.time()

            # wait until click
            while not left_click_pressed():
                pass

            speed = round((time.time() - start_time) * 1000)  # reaction speed calculation (multiply by 1000 to convert to ms then round to make neater)
            time_taken = str(speed) + ' ms'  # turn the speed into a string to show on screen

            change_bg(blue)
            display_text(large_font, time_taken, white, X_CENTER, Y_CENTER - 100)
            display_text(smallest_font, "Click to continue", white, X_CENTER, Y_CENTER)
            click_to_continue()

            scores.append(speed)

        display_average(scores)
        click_to_continue()
        running = False


reaction_test(5)