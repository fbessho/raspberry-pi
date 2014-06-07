import pygame
import time
from positions import positions

WIDTH = 640
HEIGHT = 480
COLOR = pygame.Color(0, 0, 0)
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

    while True:
        for position in positions:
            window.fill(pygame.Color(255, 255, 255))
            draw_header(window, start_time)
            draw_fps(window)
            draw_human(window, position, face_image)
            pygame.display.update()
            fps.tick(30)

        # Quit when the close button in the window is pressed
        if pygame.QUIT in [e.type for e in pygame.event.get()]:
            break

# Draw time and score
def draw_header(window, start_time):
    # Draw elapsed time
    elapsed_sec = int(time.time() - start_time)
    time_surface = HEADER_FONT.render("Elapsed Time: %d" % elapsed_sec, 1, COLOR)
    window.blit(time_surface, (10, 10))

    # Draw score
    score = elapsed_sec * 100
    score_surface = HEADER_FONT.render("Score: %d" % score, 1, COLOR)
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

    fps_surface = HEADER_FONT.render("fps: %d" % fps, 1, COLOR)
    window.blit(fps_surface, (WIDTH-20*7, HEIGHT-35)) # 20*7 = (pixels of 1 char) * (num of characters)

def draw_human(window, position, face_image):
    normalized_points = normalize(position, WIDTH/2)
    (face_center,    neck,   back,   hip,
     r_elbow, r_hand, r_knee, r_ankle, r_toe, 
     l_elbow, l_hand, l_knee, l_ankle, l_toe) = normalized_points

    # draw face
    face_width, face_height = face_image.get_size()
    face_top = face_center[0] - face_width/2
    face_left = face_center[1] - face_height/2
    window.blit(face_image, (face_top, face_left))

    # draw lines
    pygame.draw.line(window, COLOR, neck, back, LINE_WIDTH)
    pygame.draw.line(window, COLOR, back, hip,  LINE_WIDTH)

    pygame.draw.line(window, COLOR, neck,    r_elbow, LINE_WIDTH)
    pygame.draw.line(window, COLOR, r_elbow, r_hand,  LINE_WIDTH)
    pygame.draw.line(window, COLOR, hip,     r_knee,  LINE_WIDTH)
    pygame.draw.line(window, COLOR, r_knee,  r_ankle, LINE_WIDTH)
    pygame.draw.line(window, COLOR, r_ankle, r_toe,   LINE_WIDTH)

    pygame.draw.line(window, COLOR, neck,    l_elbow, LINE_WIDTH)
    pygame.draw.line(window, COLOR, l_elbow, l_hand,  LINE_WIDTH)
    pygame.draw.line(window, COLOR, hip,     l_knee,  LINE_WIDTH)
    pygame.draw.line(window, COLOR, l_knee,  l_ankle, LINE_WIDTH)
    pygame.draw.line(window, COLOR, l_ankle, l_toe,   LINE_WIDTH)

    # print(normalized_points)

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


