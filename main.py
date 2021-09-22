import pygame
from pygame import display, time, draw
import numpy as np
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
VIOLET = (46, 14, 66)
BOIDCOLOR = GREEN
BOIDRADIUS = 5
N_BOIDS = 50
BOID_SPEED = 0.01
NEAREST_RADIUS = 100

class Boid:
    def __init__(self) -> None:
        self.position = np.array([random.randint(0, WIDTH), random.randint(0, HEIGHT)], dtype=np.float32)
        self.velocity = np.array([0.0, 0.0], dtype=np.float32)
        self.acceleration = np.array([0.0, 0.0], dtype=np.float32)

    def update(self) -> None:
        if self.position[0] > WIDTH:
            self.position[0] = 0.0
        if self.position[0] < 0.0:
            self.position[0] = WIDTH
        if self.position[1] > HEIGHT:
            self.position[1] = 0.0
        if self.position[1] < 0.0:
            self.position[1] = HEIGHT
        # self.acceleration = np.clip(self.acceleration, [0,0], [BOID_SPEED, BOID_SPEED])
        self.position += self.velocity*BOID_SPEED
        self.velocity += self.acceleration
        self.acceleration = 0

    def draw(self, surface) -> None:
        draw.circle(surface, BOIDCOLOR, self.position, BOIDRADIUS)
        # draw.line(surface, BLUE, self.position, self.position+self.velocity, 1)
        # draw.line(surface, RED, self.position, self.position+self.acceleration, 1)

    def cohesion(self, flock):
        steer = np.array([0.0,0.0])
        i = 1
        for other in flock:
            if other != self:
                if distance(self.position, other.position) < NEAREST_RADIUS:
                    steer += other.position
                    i+=1
        steer /= i
        return steer - self.position
    
    def alignment(self, flock):
        steer = np.array([0.0,0.0])
        i = 1
        for other in flock:
            if other != self:
                if distance(self.position, other.position) < NEAREST_RADIUS:
                    steer += other.velocity
                    i+=1
        steer /= i
        return steer - self.velocity

def distance(a, b):
    return np.sum(np.abs(a-b)**2)**(1/2)

def draw_all(boids: list[Boid], surface):
    for boid in boids:
        boid.draw(surface)

def update_all(boids: list[Boid]):
    for boid in boids:
        boid.update()

def calculate_all(boids: list[Boid]):
    for boid in boids:
        total_steer = np.array([0.0,0.0])
        cohesion_steer = boid.cohesion(boids)
        alignment_steer = boid.alignment(boids)
        total_steer += cohesion_steer
        total_steer += alignment_steer
        boid.acceleration += total_steer/2

if __name__ == '__main__':
    pygame.init()
    display.init()
    screen = display.set_mode((WIDTH, HEIGHT))
    display.set_caption('boids')
    clock = time.Clock()
    running = True

    flock = [Boid() for _ in range(N_BOIDS)]

    while running:
        clock.tick(FPS)
        screen.fill(VIOLET)
        draw_all(flock, screen)
        pos = pygame.mouse.get_pos()
        if pos[0] > WIDTH/2:
            update_all(flock)
            calculate_all(flock)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                new = []
                if(event.key == pygame.K_q):
                    pygame.quit()
                    exit(0)
        display.update()