import pygame
from mute_button import draw_mute_button, handle_mute_button_click

_start_button_rect = None

def draw_welcome_screen(screen, screen_width, screen_height, is_muted):
    """Draw the welcome home screen."""
    global _start_button_rect
    
    # Draw background
    screen.fill((25, 140, 230))
    
    # Draw welcome title
    title_font = pygame.font.SysFont(None, 68, bold=True)
    title_text = title_font.render("MIT Sea Grant Display Tank Explorer", True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen_width // 2, 150))
    screen.blit(title_text, title_rect)
    
    # Draw subtitle
    subtitle_font = pygame.font.SysFont(None, 36)
    subtitle_text = subtitle_font.render("Discover the New England intertidal zone!", True, (200, 220, 255))
    subtitle_rect = subtitle_text.get_rect(center=(screen_width // 2, 240))
    screen.blit(subtitle_text, subtitle_rect)
    
    # Draw description
    desc_font = pygame.font.SysFont(None, 28)
    desc_lines = [
        "Explore different species of invertebrates and aquatic life.",
        "Hover over creatures to see their names.",
        "Click on any creature to learn more about them.",   
    ]

    desc_y = 320
    for line in desc_lines:
        desc_text = desc_font.render(line, True, (180, 200, 220))
        desc_rect = desc_text.get_rect(center=(screen_width // 2, desc_y))
        screen.blit(desc_text, desc_rect)
        desc_y += 40
    
    # Draw start button
    button_width = 250
    button_height = 60
    button_x = (screen_width - button_width) // 2
    button_y = 550
    _start_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    pygame.draw.rect(screen, (100, 150, 200), _start_button_rect)
    pygame.draw.rect(screen, (255, 255, 255), _start_button_rect, 3)
    
    button_text = pygame.font.SysFont(None, 36).render("Start Exploring", True, (255, 255, 255))
    button_text_rect = button_text.get_rect(center=_start_button_rect.center)
    screen.blit(button_text, button_text_rect)
    
    # Draw mute button
    draw_mute_button(screen, screen_width, is_muted)

# Checks mouse clicks on welcome screen buttons
def handle_welcome_click(pos, is_muted):
    """Handle clicks on the welcome screen."""
    mute_result = handle_mute_button_click(pos, is_muted)
    if mute_result is not None:
        return ("mute", mute_result)
    if _start_button_rect and _start_button_rect.collidepoint(pos):
        return ("start", None)
    return (None, is_muted)