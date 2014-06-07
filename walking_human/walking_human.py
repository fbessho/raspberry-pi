import pygame
import time
from positions import positions
from human import Human
from pygame.locals import *

WIDTH = 640
HEIGHT = 480
COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)
LINE_WIDTH = 4
SEC_PER_FRAME = 0.1
HEADER_FONT = None # initialized after pygame.init()

def main():
    pygame.init()
    global HEADER_FONT
    HEADER_FONT = pygame.font.SysFont("freeserif", 25, bold=1)
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    face_image = pygame.image.load("face.png")
    face_image.convert_alpha()
    fps = pygame.time.Clock()

    start_time = time.time()
    human = Human()

    while True:
        quit_flag = False
        for position in positions:
            quit_flag = handle_event(human)
            if quit_flag:
                return

            window.fill(COLOR_WHITE)
            draw_header(window, start_time)
            draw_fps(window)
            draw_human(window, position, face_image, human)
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

def draw_human(window, position, face_image, human):
    human_size = 200, HEIGHT
    human_surface = pygame.Surface(human_size)
    human_surface.fill(COLOR_WHITE)

    normalized_points = normalize(position, human_size[0]/2)
    (face_center,    neck,   back,   hip,
     r_elbow, r_hand, r_knee, r_ankle, r_toe, 
     l_elbow, l_hand, l_knee, l_ankle, l_toe) = normalized_points

    # draw face
    face_width, face_height = face_image.get_size()
    face_left = face_center[0] - face_width/2
    face_top = face_center[1] - face_height/2
    human_surface.blit(face_image, (face_left, face_top))

    # draw lines
    pygame.draw.line(human_surface, COLOR_BLACK, neck, back, LINE_WIDTH)
    pygame.draw.line(human_surface, COLOR_BLACK, back, hip,  LINE_WIDTH)

    pygame.draw.line(human_surface, COLOR_BLACK, neck,    r_elbow, LINE_WIDTH)
    pygame.draw.line(human_surface, COLOR_BLACK, r_elbow, r_hand,  LINE_WIDTH)
    pygame.draw.line(human_surface, COLOR_BLACK, hip,     r_knee,  LINE_WIDTH)
    pygame.draw.line(human_surface, COLOR_BLACK, r_knee,  r_ankle, LINE_WIDTH)
    pygame.draw.line(human_surface, COLOR_BLACK, r_ankle, r_toe,   LINE_WIDTH)

    pygame.draw.line(human_surface, COLOR_BLACK, neck,    l_elbow, LINE_WIDTH)
    pygame.draw.line(human_surface, COLOR_BLACK, l_elbow, l_hand,  LINE_WIDTH)
    pygame.draw.line(human_surface, COLOR_BLACK, hip,     l_knee,  LINE_WIDTH)
    pygame.draw.line(human_surface, COLOR_BLACK, l_knee,  l_ankle, LINE_WIDTH)
    pygame.draw.line(human_surface, COLOR_BLACK, l_ankle, l_toe,   LINE_WIDTH)

    # print(normalized_points)

    # Human directs left as default. Flip image when "right" is set as the direction.
    if human.direction.lower().startswith("r"):
        human_surface = pygame.transform.flip(human_surface,
                                              True, # xbool
                                              False # ybool
        )

    window.blit(human_surface, (WIDTH/2 - human_size[0]/2, 0))

# Set x of human's face to center, and convert float to int
def normalize(points, center):
    face_x = points[0][0]
    dx = center - face_x # px needs to shift
    normalized_points = []

    for point in points:
        normalized_points.append(
            (int(point[0] + dx), int(point[1]))
        )

    return normalized_points

if __name__ == "__main__":
    main()


