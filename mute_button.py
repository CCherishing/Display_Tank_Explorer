import pygame

_mute_button_rect = None

def draw_mute_button(screen, screen_width, is_muted):
    """Draw the mute button."""
    global _mute_button_rect
    button_width = 125
    button_height = 50
    button_x = screen_width - button_width - 10
    button_y = 10
    _mute_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
    
    pygame.draw.rect(screen, (100, 100, 100), _mute_button_rect)
    pygame.draw.rect(screen, (255, 255, 255), _mute_button_rect, 2)
    
    mute_text = "Mute" if not is_muted else "Unmute"
    mute_font = pygame.font.SysFont(None, 28)
    # Use text as fallback if emoji doesn't work
    if is_muted:
        mute_label = mute_font.render(mute_text, True, (255, 100, 100))
    else:
        mute_label = mute_font.render(mute_text, True, (100, 255, 100))
    
    text_rect = mute_label.get_rect(center=_mute_button_rect.center)
    screen.blit(mute_label, text_rect)


def handle_mute_button_click(pos, is_muted):
    """Handle clicks on the mute button. 
       Volume is at 100% or 0%.
    """
    if _mute_button_rect and _mute_button_rect.collidepoint(pos):
        is_muted = not is_muted
        if is_muted:
            pygame.mixer.music.set_volume(0)
        else:
            pygame.mixer.music.set_volume(1.0)
        return is_muted
    return None

