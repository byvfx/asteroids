import pygame
from circleshape import CircleShape
from constants import *
from bullet import Bullet

class Player(CircleShape):
    def __init__(self, x, y,):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.bullet_cooldown = 0
    
    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def rotate(self, direction, dt):
        self.rotation += direction * PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Update bullet cooldown
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= dt

        if keys[pygame.K_a]:
            self.rotate(-1, dt)
        if keys[pygame.K_d]:
            self.rotate(1, dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE] and self.bullet_cooldown <= 0:
            self.shoot()
      
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
    
    def shoot(self):
        # Create direction vector
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        # Get bullet spawn position (at the front of the ship)
        bullet_pos = self.position + forward * self.radius
        # Create new bullet
        Bullet(bullet_pos.x, bullet_pos.y, forward)
        # Reset cooldown
        self.bullet_cooldown = BULLET_COOLDOWN
