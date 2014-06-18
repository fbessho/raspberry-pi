import pygame
import time
from human import Human
from pygame.locals import *
import pdb

WIDTH = 640
HEIGHT = 480
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)
SEC_PER_FRAME = 0.1
HEADER_FONT = None # initialized after pygame.init()

def main():
    pygame.init()
    global HEADER_FONT
    HEADER_FONT = pygame.font.SysFont("freeserif", 25, bold=1)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    fps = pygame.time.Clock()

    start_time = time.time()
    human = Human()
    human.setDaemon(True)
    human.start()

    while True:
        quit_flag = handle_event(human)
        if quit_flag:
            return

        window.fill(COLOR_WHITE)
        draw_header(window, start_time)
        draw_fps(window)
        # pdb.set_trace()
        human.draw(window)
        pygame.display.update()
        fps.tick(30)

# Returns True if program should exit
def handle_event(human):
    for event in pygame.event.get():
        # Quit when the close button in the window is pressed
        if event.type == pygame.QUIT:
            return True
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                return True
            if event.key == K_RIGHT:
                human.direction = "right"
            if event.key == K_LEFT:
                human.direction = "left"

    return False

# Draw time and score
def draw_header(window, start_time):
    # Draw elapsed time
    elapsed_sec = int(time.time() - start_time)
    time_surface = HEADER_FONT.render("Elapsed Time: %d" % elapsed_sec, 1, COLOR_BLACK)
    window.blit(time_surface, (10, 10))

    # Draw score
    score = elapsed_sec * 100
    score_surface = HEADER_FONT.render("Score: %d" % score, 1, COLOR_BLACK)
    window.blit(score_surface, (WIDTH-240, 10))

# Draw fps at bottom-right
def draw_fps(window):
    if not hasattr(draw_fps, 'frame_time_previous'):
        draw_fps.frame_time_previous = time.time()
        return

    previous_time = draw_fps.frame_time_previous
    current_time = time.time()
    draw_fps.frame_time_previous = current_time
    fps = 1 / (current_time - previous_time)

    fps_surface = HEADER_FONT.render("fps: %d" % fps, 1, COLOR_BLACK)
    window.blit(fps_surface, (WIDTH-20*7, HEIGHT-35)) # 20*7 = (pixels of 1 char) * (num of characters)



if __name__ == "__main__":
    main()


