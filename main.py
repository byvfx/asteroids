import pygame
from constants import *
from player import Player


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    # Create a player at the center of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
                
        # Clear the screen
        screen.fill((0, 0, 0))
        
        # Draw the player
        player.draw(screen)
        
        # Update the display
        pygame.display.flip()
        
        # Control the frame rate
        dt = clock.tick(60)/1000
        # Use dt in game logic here, e.g., updating positions:
        # object.update(dt)
       
    print("Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")


if __name__ == "__main__":
    main()
