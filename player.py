import pygame
import math
from circleshape import CircleShape
from constants import *
from bullet import Bullet

# Helper functions for triangle collision
def point_in_triangle(p, triangle):
    """Check if point p is inside triangle"""
    a, b, c = triangle
    
    def sign(p1, p2, p3):
        return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
    
    d1 = sign(p, a, b)
    d2 = sign(p, b, c)
    d3 = sign(p, c, a)
    
    has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
    has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)
    
    # If all signs are the same, point is inside
    return not (has_neg and has_pos)

def line_circle_collision(p1, p2, circle_center, circle_radius):
    """Check if line segment from p1 to p2 intersects with circle"""
    # Vector from p1 to p2
    line_vec = pygame.Vector2(p2.x - p1.x, p2.y - p1.y)
    line_len = line_vec.length()
    
    # Vector from p1 to circle center
    circle_vec = pygame.Vector2(circle_center.x - p1.x, circle_center.y - p1.y)
    
    # Normalized line vector
    if line_len > 0:
        line_unit = line_vec / line_len
    else:
        return circle_vec.length() <= circle_radius
    
    # Project circle_vec onto line_unit
    projection_len = circle_vec.dot(line_unit)
    
    # Get closest point on line segment
    if projection_len < 0:
        closest_point = pygame.Vector2(p1.x, p1.y)
    elif projection_len > line_len:
        closest_point = pygame.Vector2(p2.x, p2.y)
    else:
        closest_point = pygame.Vector2(p1.x, p1.y) + line_unit * projection_len
    
    # Check if distance from closest point to circle center is less than radius
    closest_dist = (closest_point - circle_center).length()
    return closest_dist <= circle_radius

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
    
    def collides_with(self, other):
        # Override the circular collision with triangle-circle collision
        # Get the triangle points
        triangle_points = self.triangle()
        
        # First check if the other object's center is inside the triangle
        if point_in_triangle(other.position, triangle_points):
            return True
            
        # Then check if any of the triangle edges intersect with the circle
        for i in range(3):
            p1 = triangle_points[i]
            p2 = triangle_points[(i + 1) % 3]
            
            # Check distance from line segment to circle center
            if line_circle_collision(p1, p2, other.position, other.radius):
                return True
                
        return False
    
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
