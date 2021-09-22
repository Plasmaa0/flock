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
BOID_SPEED = 10
NEAREST_RADIUS = 100
MAX_SPEED = 100

class Boid:
    def __init__(self) -> None:
        self.position = np.array([random.randint(0, WIDTH), random.randint(0, HEIGHT)], dtype=np.float32)
        self.velocity = np.array([0.0, 0.0], dtype=np.float32)
        self.acceleration = np.array([0.0, 0.0], dtype=np.float32)

    def edges(self):
        if self.position[0] > WIDTH:
            self.position[0] = 0.0
        if self.position[0] < 0.0:
            self.position[0] = WIDTH
        if self.position[1] > HEIGHT:
            self.position[1] = 0.0
        if self.position[1] < 0.0:
            self.position[1] = HEIGHT

    def update(self) -> None:
        self.position += self.velocity
        self.velocity += self.acceleration
        self.acceleration = 0
        if np.max(self.velocity) > MAX_SPEED:
            self.velocity /= np.max(self.velocity)

    def draw(self, surface) -> None:
        draw.circle(surface, BOIDCOLOR, self.position, BOIDRADIUS)
        # draw.line(surface, BLUE, self.position, self.position+self.velocity, 1)
        # draw.line(surface, RED, self.position, self.position+self.acceleration, 1)

    def cohesion(self, flock):
        steer = np.array([0.0,0.0], dtype=np.float32)
        i = 1
        for other in flock:
            if other != self:
                if distance(self.position, other.position) < NEAREST_RADIUS:
                    steer += other.position
                    i+=1
        steer /= i
        return steer
    
    def alignment(self, flock):
        steer = np.array([0.0,0.0], dtype=np.float32)
        i = 1
        for other in flock:
            if other != self:
                if distance(self.position, other.position) < NEAREST_RADIUS:
                    steer += other.velocity
                    i+=1
        steer /= i
        return steer

def distance(a, b):
    return np.sum(np.abs(a-b)**2)**(1/2)

def draw_all(boids: list[Boid], surface):
    for boid in boids:
        boid.draw(surface)

def update_all(boids: list[Boid]):
    for boid in boids:
        boid.update()
        boid.edges()

def calculate_all(boids: list[Boid]):
    for boid in boids:
        total_steer = np.array([0.0,0.0], dtype=np.float32)
        cohesion_steer = boid.cohesion(boids)
        alignment_steer = boid.alignment(boids)
        total_steer += cohesion_steer
        total_steer += alignment_steer
        boid.acceleration += total_steer

if __name__ == '__main__':
    pygame.init()
    display.init()
    screen = display.set_mode((WIDTH, HEIGHT))
    display.set_caption('boids')
    clock = time.Clock()
    running = True

    flock = [Boid() for _ in range(N_BOIDS)]

    up = -1
    while running:
        clock.tick(FPS)
        screen.fill(VIOLET)
        draw_all(flock, screen)
        pos = pygame.mouse.get_pos()
        if up == 1:
            update_all(flock)
            calculate_all(flock)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                new = []
                if(event.key == pygame.K_q):
                    pygame.quit()
                    exit(0)
                if event.key == pygame.K_p:
                    up *= -1
                if event.key == pygame.K_0:
                    MAX_SPEED += 200
                if event.key == pygame.K_9:
                    MAX_SPEED -= 20
                
        display.update()