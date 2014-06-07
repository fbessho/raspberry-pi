import pygame
from time import sleep
from positions import positions

WIDTH = 640
HEIGHT = 480
COLOR = pygame.Color(255, 0, 0)
SEC_PER_FRAME = 0.1

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    while True:
        for position in positions:
            draw_human(window, position)
            sleep(SEC_PER_FRAME)

def draw_human(window, position):
    normalized_points = normalize(position, WIDTH/2)
    (head_center,    neck,   back,   hip,
     r_elbow, r_hand, r_knee, r_ankle, r_toe, 
     l_elbow, l_hand, l_knee, l_ankle, l_toe) = normalized_points

    window.fill(pygame.Color(255, 255, 255))

    # draw head
    head_width, head_height = 47, 55
    head_top = head_center[0] - head_width/2
    head_left = head_center[1] - head_height/2
    pygame.draw.ellipse(window, 
                        COLOR,
                        pygame.Rect(head_top, head_left, head_width, head_height),
                        1)

    # draw lines
    pygame.draw.line(window, COLOR, neck, back, 1)
    pygame.draw.line(window, COLOR, back, hip,  1)

    pygame.draw.line(window, COLOR, neck,    r_elbow, 1)
    pygame.draw.line(window, COLOR, r_elbow, r_hand,  1)
    pygame.draw.line(window, COLOR, hip,     r_knee,  1)
    pygame.draw.line(window, COLOR, r_knee,  r_ankle, 1)
    pygame.draw.line(window, COLOR, r_ankle, r_toe,   1)

    pygame.draw.line(window, COLOR, neck,    l_elbow, 1)
    pygame.draw.line(window, COLOR, l_elbow, l_hand,  1)
    pygame.draw.line(window, COLOR, hip,     l_knee,  1)
    pygame.draw.line(window, COLOR, l_knee,  l_ankle, 1)
    pygame.draw.line(window, COLOR, l_ankle, l_toe,   1)

    # print(normalized_points)
    pygame.display.update()

# Set x of human's head to center, and convert float to int
def normalize(points, center):
    head_x = points[0][0]
    dx = center - head_x # px needs to shift
    normalized_points = []

    for point in points:
        normalized_points.append(
            (int(point[0] + dx), int(point[1]))
        )

    return normalized_points


main()


