import pygame
from constants import *
from player import Player
from asteroidfield import AsteroidField
from asteroid import Asteroid
from bullet import Bullet


def show_game_over(screen):
    """Display the game over screen"""
    # Fill screen with black
    screen.fill((0, 0, 0))
    
    # Create font objects
    try:
        font_big = pygame.font.SysFont('Arial', 64)
        font_small = pygame.font.SysFont('Arial', 32)
    except:
        font_big = pygame.font.Font(None, 64)
        font_small = pygame.font.Font(None, 32)
    
    # Render text
    game_over_text = font_big.render("GAME OVER", True, (255, 0, 0))
    restart_text = font_small.render("Press R to restart", True, (255, 255, 255))
    quit_text = font_small.render("Press Q to quit", True, (255, 255, 255))
    
    # Position text
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 80))
    
    # Draw text
    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(quit_text, quit_rect)
    
    # Update display
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Asteroids")
    
    def start_game():
        # Create sprite groups
        updatable = pygame.sprite.Group()
        drawable = pygame.sprite.Group()
        asteroids = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        
        # Set the groups as containers
        Player.containers = (updatable, drawable)
        Asteroid.containers = (updatable, drawable, asteroids)
        Bullet.containers = (updatable, drawable, bullets)
        AsteroidField.containers = (updatable,)
        
        # Create a player at the center of the screen
        player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        
        # Create the asteroid field to spawn asteroids
        AsteroidField()
        
        return player, updatable, drawable, asteroids, bullets
    
    player, updatable, drawable, asteroids, bullets = start_game()
    game_over = False
    score = 0
    
    # Initialize font for score display
    try:
        font = pygame.font.SysFont('Arial', 24)
    except:
        font = pygame.font.Font(None, 24)  # Use default font
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
            if game_over:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        # Restart game
                        player, updatable, drawable, asteroids, bullets = start_game()
                        game_over = False
                        score = 0
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        return
        
        if game_over:
            # Show game over screen while in game over state
            show_game_over(screen)
            continue
        
        # Control the frame rate and get dt
        dt = clock.tick(60)/1000
        
        # Update all objects
        updatable.update(dt)
        
        # Check for collisions between player and asteroids
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                game_over = True
                break
        
        # Check for collisions between bullets and asteroids
        for bullet in bullets:
            asteroid_hit = None
            
            for asteroid in asteroids:
                if bullet.collides_with(asteroid):
                    asteroid_hit = asteroid
                    bullet.kill()
                    score += 100  # Add points for hitting asteroid
                    break
            
            if asteroid_hit:
                # Split the asteroid
                new_asteroids = asteroid_hit.split()
                asteroid_hit.kill()
                
                # Add smaller asteroids to groups
                for new_asteroid in new_asteroids:
                    pass  # New asteroids are automatically added to groups through __init__
                
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw all objects
        for sprite in drawable:
            sprite.draw(screen)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        
        # Update the display
        pygame.display.flip()


if __name__ == "__main__":
    main()
