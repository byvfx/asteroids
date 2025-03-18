import pygame
import math
from circleshape import CircleShape
from constants import *

class Bullet(CircleShape):
    def __init__(self, x, y, direction):
        super().__init__(x, y, BULLET_RADIUS)
        self.velocity = direction * BULLET_SPEED
        self.lifetime = 0
        self.max_lifetime = 2.0  # seconds until bullet disappears
        
    def triangle(self):
        # For bullet we'll just return a simple circle outline points
        points = []
        num_points = 8
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            x = self.position.x + self.radius * math.cos(angle)
            y = self.position.y + self.radius * math.sin(angle)
            points.append((x, y))
        return points
    
    def update(self, dt):
        super().update(dt)
        
        # Update lifetime and kill if too old
        self.lifetime += dt
        if self.lifetime > self.max_lifetime:
            self.kill()
            
        # Kill if off screen
        if (self.position.x < -self.radius or 
            self.position.x > SCREEN_WIDTH + self.radius or
            self.position.y < -self.radius or 
            self.position.y > SCREEN_HEIGHT + self.radius):
            self.kill()