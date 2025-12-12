import pygame

_home_button_rect = None
_game_state = None

def draw_home_button(surface):
    """Draw the 'Back to Home' button on the game screen."""
    global _home_button_rect
    button_width = 160
    button_height = 40
    button_x = 10
    button_y = 10
    _home_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    pygame.draw.rect(surface, (100, 100, 100), _home_button_rect)
    pygame.draw.rect(surface, (255, 255, 255), _home_button_rect, 2)
    
    button_font = pygame.font.SysFont(None, 24)
    button_text = button_font.render("Back to Home", True, (255, 255, 255))
    text_rect = button_text.get_rect(center=_home_button_rect.center)
    surface.blit(button_text, text_rect)

def handle_home_button_click(pos):
    """Handle clicks on the home button.
       If clicked, returns to welcome screen.
    """
    if _home_button_rect and _home_button_rect.collidepoint(pos):
        return True
    return False
