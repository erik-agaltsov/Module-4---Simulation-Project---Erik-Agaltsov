import math
import random
import pygame

# Simulation Constants
WIDTH, HEIGHT = 800, 600
NUM_CELLS = 50
GREEN = (66, 244, 95)
RED = (244, 65, 65)
CELL_RADIUS = 7
FPS = 60

# Spatial Geometry Concepts
class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
    
    def distance(self, other_point):
        return math.sqrt((self.x - other_point.x) ** 2 + (self.y - other_point.y) ** 2)
    
    def move(self, vector):
        self.x += vector.h
        self.y += vector.v

# Physics & Movement Vectors
class Vector:
    def __init__(self, h, v):
        self.h = float(h)
        self.v = float(v)
      
    def add(self, otherVector):
        self.h += otherVector.h
        self.v += otherVector.v

    def subtract(self, otherVector):
        self.h -= otherVector.h
        self.v -= otherVector.v

    def multiply(self, scalar):
        self.h *= scalar
        self.v *= scalar

    def divide(self, scalar):
        if scalar != 0:
            self.h /= scalar
            self.v /= scalar

    def length(self):
        return math.sqrt(self.h ** 2 + self.v ** 2)

    def normalize(self):
        len_val = self.length()
        if len_val != 0:
            self.divide(len_val)

# Agent / Entity Logic
class Cell:
    def __init__(self, color):
        x = random.randint(CELL_RADIUS, WIDTH - CELL_RADIUS)
        y = random.randint(CELL_RADIUS, HEIGHT - CELL_RADIUS)
        self.location = Point(x, y)
        self.pos = self.location
        
        h = random.uniform(-1, 1)
        v = random.uniform(-1, 1)
        self.velocity = Vector(h, v)
        self.velocity.normalize()
        self.velocity.multiply(random.uniform(1, 2))
        
        self.size = CELL_RADIUS
        self.color = color

    def move_cell(self, cells):
        self.pos.move(self.velocity)

        if self.pos.x - self.size < 0:
            self.pos.x = self.size
            self.velocity.h *= -1
        elif self.pos.x + self.size > WIDTH:
            self.pos.x = WIDTH - self.size
            self.velocity.h *= -1

        if self.pos.y - self.size < 0:
            self.pos.y = self.size
            self.velocity.v *= -1
        elif self.pos.y + self.size > HEIGHT:
            self.pos.y = HEIGHT - self.size
            self.velocity.v *= -1

        for othercell in cells:
            if othercell != self:
                dist = self.pos.distance(othercell.pos)
                if dist < (2 * self.size):
                    if self.color == GREEN and othercell.color == RED:
                        self.color = RED

    def draw_cell(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.location.x), int(self.location.y)), self.size)

# Simulation Setup & Population
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Virus Simulation")

def reset_simulation():
    cells = []
    for _ in range(NUM_CELLS - 1):
        cells.append(Cell(GREEN))
    cells.append(Cell(RED))
    return cells

# Initialize the simulation
cells = reset_simulation()

# Data collection
trial_count = 0
max_trials = 100
data_file = "sim1_data.txt"
with open(data_file, "w") as file:
    pass

running = True
clock = pygame.time.Clock()
frames = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((0, 0, 0))
    
    all_infected = all(cell.color == RED for cell in cells)
    if all_infected:
        seconds = frames / FPS
        with open(data_file, "a") as file:
            file.write(f"{seconds}\n")
        
        trial_count += 1
        if trial_count >= max_trials:
            running = False
        else:
            cells = reset_simulation()
            frames = 0

    for cell in cells:
        cell.move_cell(cells)
        
    for cell in cells:
        cell.draw_cell(screen)
    
    pygame.display.flip()
    clock.tick(FPS)
    frames += 1

pygame.quit()