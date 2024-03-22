import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Digital Sandbox World")

# Define colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Load font
font = pygame.font.SysFont(None, 60)

# Display welcome message
welcome_text_surface = font.render('Welcome...', True, GREEN)
welcome_text_rect = welcome_text_surface.get_rect(center=(WIDTH/2, HEIGHT/2 - 50))

# Display "Click to Enter" button
button_text_surface = font.render('Click to Enter', True, GREEN)
button_text_rect = button_text_surface.get_rect(center=(WIDTH/2, HEIGHT/2 + 50))

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is clicked on the button
            if button_text_rect.collidepoint(event.pos):
                print("Entering sandbox world...")  # Placeholder action for entering the sandbox world

    # Fill the screen with black color
    screen.fill(BLACK)
    
    # Draw the welcome message and button
    screen.blit(welcome_text_surface, welcome_text_rect)
    screen.blit(button_text_surface, button_text_rect)

    # Update the display
    pygame.display.flip()
