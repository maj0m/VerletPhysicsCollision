import pygame
import math
import random

class Circle:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.oldX = self.x
        self.oldY = self.y
        self.forceX = 0
        self.forceY = 0

        self.radius = radius
        self.color = (random.randint(120, 255), random.randint(120, 180), random.randint(120, 140))
        self.mass = 1
        self.bounciness = 0.1


    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)


    def update(self, dt):
        # Verlet integration
        velX = self.x - self.oldX
        velY = self.y - self.oldY

        self.oldX = self.x
        self.oldY = self.y

        accX = self.forceX / self.mass
        accY = self.forceY / self.mass

        self.x += velX + accX * dt * dt
        self.y += velY + accY * dt * dt

        self.forceX = 0
        self.forceY = 0


    def constrain(self, width, height):
        # Don't go off the screen
        velX = (self.x - self.oldX) * self.bounciness
        velY = (self.y - self.oldY) * self.bounciness

        if self.x < self.radius:
            self.x = self.radius
            self.oldX = self.x + velX
        if self.x > width - self.radius:
            self.x = width - self.radius
            self.oldX = self.x + velX
        if self.y < self.radius:
            self.y = self.radius
            self.oldY = self.y + velY
        if self.y > height - self.radius:
            self.y = height - self.radius
            self.oldY = self.y + velY


    def apply_force(self, force):
        self.forceX += force[0]
        self.forceY += force[1]


    def collide_with(self, other):
        dist_x = self.x - other.x
        dist_y = self.y - other.y
        dist_squared = dist_x * dist_x + dist_y * dist_y

        # Only calculate square root if dist_squared < radii_squared
        if dist_squared < (self.radius + other.radius) ** 2 and dist_squared != 0:
            dist = math.sqrt(dist_squared)
            dir_x = dist_x / dist
            dir_y = dist_y / dist
            overlap = self.radius + other.radius - dist
            pushback = overlap / 2

            self.x  += dir_x * pushback
            self.y  += dir_y * pushback
            other.x -= dir_x * pushback
            other.y -= dir_y * pushback

    
