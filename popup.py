import pygame
import os
from load_helpers import load_image_surface

_popup_state = None

def get_popup_state():
    """Get the current popup state."""
    return _popup_state

# Ensures text fits within given width by wrapping lines
def wrap_text(text, max_width, font):
    """Wrap text to fit within max_width."""
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        if font.size(test_line)[0] <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines


def open_popup(species_obj):
    """Open a popup window with species details."""
    global _popup_state
    # Dictionary to hold popup info
    _popup_state = {
        "id": species_obj["id"],
        "common_name": species_obj["common_name"],
        "scientific_name": species_obj["scientific_name"],
        "description": species_obj["description"],
        "habitat_info": species_obj["habitat_info"],
        "s_image": species_obj.get("s_image", ""),
        "native_status": species_obj.get("native_status", ""),
        "fun_fact": species_obj.get("fun_fact", ""),
        "x": species_obj["x"],
        "y": species_obj["y"],
        "sprite_path": species_obj.get("sprite_path", ""),
        "tab": 0  # Default to Description tab
    }
    
    # Log popup open
    print(f"[POPUP] Opened '{species_obj['common_name']}' - Image path: '{species_obj['s_image']}' (Exists: {os.path.exists(species_obj['s_image'])})")

    return _popup_state
    
def close_popup():
    """Close the currently open popup."""
    global _popup_state
    _popup_state = None
    
    return _popup_state

# Pop-Up window after clicking species sprite
def draw_popup(screen, screen_width, screen_height, popup_width, popup_height, popup_bg_color, popup_border_color, text_color, popup_state):
    """Draw the popup window on screen."""
    if popup_state is None:
        return
    
    # Calculate centered position
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2
    
    # Draw semi-transparent overlay
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 100))
    screen.blit(overlay, (0, 0))
    
    # Draw popup background
    popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
    pygame.draw.rect(screen, popup_bg_color, popup_rect)
    pygame.draw.rect(screen, popup_border_color, popup_rect, 3)
    
    # Draw title
    title_font = pygame.font.SysFont(None, 35, bold=True)
    title_text = title_font.render(popup_state["common_name"], True, (255, 255, 255))
    title_rect = title_text.get_rect(center=(screen_width // 2, popup_y + 20))
    screen.blit(title_text, title_rect)
    
    # Draw tab buttons
    tab_y = popup_y + 50
    tabs = ["Description", "Habitat"]
    tab_width = popup_width // 2
    tab_font = pygame.font.SysFont(None, 30)
    
    for i, tab_name in enumerate(tabs):
        tab_x = popup_x + i * tab_width
        tab_rect = pygame.Rect(tab_x, tab_y, tab_width, 30)
        
        if i == popup_state["tab"]:
            pygame.draw.rect(screen, (100, 150, 200), tab_rect)
        else:
            pygame.draw.rect(screen, (180, 180, 180), tab_rect)
        
        pygame.draw.rect(screen, popup_border_color, tab_rect, 1)
        tab_text = tab_font.render(tab_name, True, text_color)
        text_rect = tab_text.get_rect(center=tab_rect.center)
        screen.blit(tab_text, text_rect)
    
    # Draw content area
    content_y = popup_y + 90
    content_height = popup_height - 100
    content_rect = pygame.Rect(popup_x + 10, content_y, popup_width - 20, content_height)
    pygame.draw.rect(screen, (255, 255, 255), content_rect)
    pygame.draw.rect(screen, popup_border_color, content_rect, 1)
    
    # Draw tab content
    reg_font_28 = pygame.font.SysFont(None, 28)
    label_font_28 = pygame.font.SysFont(None, 28, bold=True)
    text_y = content_y + 10
    line_height = 22
    
    if popup_state["tab"] == 0:  # Description tab with image on left, info on right
        # Image on the left side
        img_width = 200
        img_height = 280
        img_x = popup_x + 20
        img_y = content_y + 10
        
        img_path = popup_state.get("s_image", "")
        if img_path and os.path.exists(img_path):
            try:
                img_surf = load_image_surface(img_path, (img_width, img_height))
                if img_surf:
                    screen.blit(img_surf, (img_x, img_y))
                    pygame.draw.rect(screen, popup_border_color, pygame.Rect(img_x, img_y, img_width, img_height), 1)
            except Exception as e:
                print(f"[ERROR] Failed to load image {img_path}: {e}")
                placeholder = pygame.Surface((img_width, img_height))
                placeholder.fill((255, 100, 100))
                screen.blit(placeholder, (img_x, img_y))
        else:
            # Red block if image not found
            placeholder = pygame.Surface((img_width, img_height))
            placeholder.fill((255, 0, 0))
            screen.blit(placeholder, (img_x, img_y))
        
        # Text on the right side
        text_x = img_x + img_width + 15
        text_width = content_rect.width - img_width - 40
        
        # Scientific name
        sci_name_label = label_font_28.render("Scientific Name:", True, text_color)
        screen.blit(sci_name_label, (text_x, text_y))
        text_y += 20
        sci_name_text = reg_font_28.render(popup_state.get("scientific_name", ""), True, text_color)
        screen.blit(sci_name_text, (text_x, text_y))
        text_y += 22
        
        # Native/Non-native status
        status_label = label_font_28.render("Status:", True, text_color)
        screen.blit(status_label, (text_x, text_y))
        text_y += 20
        status = popup_state.get("native_status", "")
        status_color = (0, 150, 0) if status == "Native" else (150, 0, 0)
        status_text = reg_font_28.render(status, True, status_color)
        screen.blit(status_text, (text_x, text_y))
        text_y += 22
        
        # Description
        desc_label = label_font_28.render("Description:", True, text_color)
        screen.blit(desc_label, (text_x, text_y))
        text_y += 20
        desc_lines = wrap_text(popup_state.get("description", ""), text_width, reg_font_28)
        for line in desc_lines[:6]:  # Limit to 6 lines
            if text_y + 20 > content_y + content_height - 10:
                break
            desc_text = reg_font_28.render(line, True, text_color)
            screen.blit(desc_text, (text_x, text_y))
            text_y += 20
        
        text_y += 2
        
        # Fun fact
        fact_label = label_font_28.render("Fun Fact:", True, text_color)
        screen.blit(fact_label, (text_x, text_y))
        text_y += 20
        # Wrap and draw text
        fact_lines = wrap_text(popup_state.get("fun_fact", ""), text_width, reg_font_28)
        for line in fact_lines[:6]:  # Allow up to 6 lines for fun fact
            if text_y + 20 > content_y + content_height - 10:
                break
            fact_text = reg_font_28.render(line, True, (60, 100, 140))
            screen.blit(fact_text, (text_x, text_y))
            text_y += 20
            
    elif popup_state["tab"] == 1:  # Habitat
        content = popup_state["habitat_info"]
        # Wrap and draw text
        lines = wrap_text(content, popup_width - 30, reg_font_28)
        for line in lines:
            if text_y + line_height > content_y + content_rect.height:
                break
            text_surf = reg_font_28.render(line, True, text_color)
            screen.blit(text_surf, (popup_x + 10, text_y))
            text_y += line_height        
    
    # Draw close button
    close_btn_rect = pygame.Rect(popup_x + popup_width - 30, popup_y + 5, 25, 25)
    pygame.draw.rect(screen, (255, 100, 100), close_btn_rect)
    pygame.draw.rect(screen, popup_border_color, close_btn_rect, 1)
    close_text = title_font.render("X", True, text_color)
    close_text_rect = close_text.get_rect(center=close_btn_rect.center)
    screen.blit(close_text, close_text_rect)
    
    # Store close button rect for click detection
    if popup_state is not None:
        popup_state["close_btn_rect"] = close_btn_rect


# Reactions from having clicked on exit or tab buttons in popup
def handle_popup_click(pos, screen_width, screen_height, popup_width, popup_height, popup_state):
    """Handle mouse clicks on the popup."""
    if popup_state is None:
        return False
    
    # Check close button
    if "close_btn_rect" in popup_state:
        if popup_state["close_btn_rect"].collidepoint(pos):
            return "close"
    
    popup_x = (screen_width - popup_width) // 2
    popup_y = (screen_height - popup_height) // 2
    tab_y = popup_y + 50
    tabs = ["Description", "Habitat"]
    tab_width = popup_width // 2
    
    # Tab locations and click detection to switch tabs
    for i, tab_name in enumerate(tabs):
        tab_x = popup_x + i * tab_width
        tab_rect = pygame.Rect(tab_x, tab_y, tab_width, 30)
        if tab_rect.collidepoint(pos):
            popup_state["tab"] = i
            return True
    return False