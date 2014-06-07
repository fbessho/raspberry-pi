import threading
import time
import pygame
from positions import positions

COLOR_BLACK = pygame.Color(0, 0, 0)
COLOR_WHITE = pygame.Color(255, 255, 255)

class Human(threading.Thread):
    WIDTH = 200
    HEIGHT = 480
    LINE_WIDTH = 4
    
    def __init__(self):
        threading.Thread.__init__(self)
        self.direction = "left"
        self.face_image = pygame.image.load("face.png")
        self.face_image.convert_alpha()
        self.surface = self.update_surface(positions[0])

    def run(self):
        while True:
            for position in positions:
                position = self.update_surface(position)
                time.sleep(0.2)

    def update_surface(self, position):
        human_size = Human.WIDTH, Human.HEIGHT
        human_surface = pygame.Surface(human_size)
        human_surface.fill(COLOR_WHITE)

        normalized_points = self.normalize(position, human_size[0]/2)
        (face_center,    neck,   back,   hip,
         r_elbow, r_hand, r_knee, r_ankle, r_toe, 
         l_elbow, l_hand, l_knee, l_ankle, l_toe) = normalized_points

        # draw face
        face_width, face_height = self.face_image.get_size()
        face_left = face_center[0] - face_width/2
        face_top = face_center[1] - face_height/2
        human_surface.blit(self.face_image, (face_left, face_top))

        # draw lines
        pygame.draw.line(human_surface, COLOR_BLACK, neck, back, Human.LINE_WIDTH)
        pygame.draw.line(human_surface, COLOR_BLACK, back, hip,  Human.LINE_WIDTH)

        pygame.draw.line(human_surface, COLOR_BLACK, neck,    r_elbow, Human.LINE_WIDTH)
        pygame.draw.line(human_surface, COLOR_BLACK, r_elbow, r_hand,  Human.LINE_WIDTH)
        pygame.draw.line(human_surface, COLOR_BLACK, hip,     r_knee,  Human.LINE_WIDTH)
        pygame.draw.line(human_surface, COLOR_BLACK, r_knee,  r_ankle, Human.LINE_WIDTH)
        pygame.draw.line(human_surface, COLOR_BLACK, r_ankle, r_toe,   Human.LINE_WIDTH)

        pygame.draw.line(human_surface, COLOR_BLACK, neck,    l_elbow, Human.LINE_WIDTH)
        pygame.draw.line(human_surface, COLOR_BLACK, l_elbow, l_hand,  Human.LINE_WIDTH)
        pygame.draw.line(human_surface, COLOR_BLACK, hip,     l_knee,  Human.LINE_WIDTH)
        pygame.draw.line(human_surface, COLOR_BLACK, l_knee,  l_ankle, Human.LINE_WIDTH)
        pygame.draw.line(human_surface, COLOR_BLACK, l_ankle, l_toe,   Human.LINE_WIDTH)

        # print(normalized_points)

        # Human directs left as default. Flip image when "right" is set as the direction.
        if self.direction.lower().startswith("r"):
            human_surface = pygame.transform.flip(human_surface,
                                                  True, # xbool
                                                  False # ybool
            )

        self.surface = human_surface

    def draw(self, window):
        window.blit(self.surface, (window.get_width()/2 - Human.WIDTH/2, 0))
    
    # Set x of human's face to center, and convert float to int
    def normalize(self, points, center):
        face_x = points[0][0]
        dx = center - face_x # px needs to shift
        normalized_points = []

        for point in points:
            normalized_points.append(
                (int(point[0] + dx), int(point[1]))
            )

        return normalized_points
