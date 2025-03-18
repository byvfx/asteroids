from circleshape import CircleShape
from constants import *
import pygame
import math
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, velocity=None):
        super().__init__(x, y, radius)
        # Create random rotation for the asteroid
        self.rotation = 0
        self.rotation_speed = math.radians(random.randint(-30, 30))
        
        # If velocity is provided, use it (for child asteroids)
        if velocity:
            self.velocity = velocity
            
    def split(self):
        # Check if asteroid is too small to split
        if self.radius <= ASTEROID_MIN_RADIUS:
            return []
            
        # Create two smaller asteroids
        new_radius = self.radius / 1.5
        new_asteroids = []
        
        # Create random velocities for the new asteroids
        for i in range(2):
            # Get a random angle for the new velocity
            angle = random.uniform(0, 2 * math.pi)
            direction = pygame.Vector2(math.cos(angle), math.sin(angle))
            speed = random.randint(60, 120)  # Slightly faster than original
            new_velocity = direction * speed
            
            # Create new asteroid
            new_asteroid = Asteroid(
                self.position.x, 
                self.position.y, 
                new_radius,
                new_velocity
            )
            new_asteroids.append(new_asteroid)
            
        return new_asteroids
        
    def triangle(self):
        # Generate points for a simple polygon shape
        points = []
        num_points = 8  # Number of points for the asteroid shape
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points + self.rotation
            # Add some randomness to make the asteroid look irregular
            radius = self.radius * (0.8 + 0.4 * ((i % 3) / 3))
            x = self.position.x + radius * math.cos(angle)
            y = self.position.y + radius * math.sin(angle)
            points.append((x, y))
        return points
        
    def update(self, dt):
        super().update(dt)
        # Rotate the asteroid
        self.rotation += self.rotation_speed * dt
        
        # Wrap around screen edges
        if self.position.x < -self.radius:
            self.position.x = SCREEN_WIDTH + self.radius
        elif self.position.x > SCREEN_WIDTH + self.radius:
            self.position.x = -self.radius
        if self.position.y < -self.radius:
            self.position.y = SCREEN_HEIGHT + self.radius
        elif self.position.y > SCREEN_HEIGHT + self.radius:
            self.position.y = -self.radius
        
    def draw(self, screen):
        # Override the parent draw method to only draw the polygon without the circle
        pygame.draw.polygon(screen, "white", self.triangle(), 2)