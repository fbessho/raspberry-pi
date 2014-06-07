import pygame
from time import sleep
from positions import positions

WIDTH = 640
HEIGHT = 480
COLOR = pygame.Color(0, 0, 0)
LINE_WIDTH = 4
SEC_PER_FRAME = 0.1

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    face_image = pygame.image.load("face.png")
    face_image.convert_alpha()

    while True:
        for position in positions:
            draw_human(window, position, face_image)
            sleep(SEC_PER_FRAME)

        # Quit when the close button in the window is pressed
        if pygame.QUIT in [e.type for e in pygame.event.get()]:
            break

def draw_human(window, position, face_image):
    normalized_points = normalize(position, WIDTH/2)
    (face_center,    neck,   back,   hip,
     r_elbow, r_hand, r_knee, r_ankle, r_toe, 
     l_elbow, l_hand, l_knee, l_ankle, l_toe) = normalized_points

    window.fill(pygame.Color(255, 255, 255))

    # draw face
    face_width, face_height = face_image.get_size()
    face_top = face_center[0] - face_width/2
    face_left = face_center[1] - face_height/2
#     pygame.draw.ellipse(window, 
#                         COLOR,
#                         pygame.Rect(face_top, face_left, face_width, face_height),
#                         1)
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
    pygame.display.update()

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


main()


