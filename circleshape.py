import pygame

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # Draw the shape using the triangle points
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def update(self, dt):
        self.position += self.velocity * dt
        
    def collides_with(self, other):
        # Check if two circle shapes are colliding
        distance = self.position.distance_to(other.position)
        return distance < (self.radius + other.radius)