import pygame
import math
import random
from load_helpers import load_species_from_csv, load_image_surface

_species_objects = []

def prepare_species_objects(species_csv, species_default_size):
    global _species_objects
    species_list = load_species_from_csv(species_csv)

    # Load sprites and create objects
    _species_objects.clear()
    for sp in species_list:
        sprite_path = sp.get("sprite")
        base_w, base_h = species_default_size
        surf = load_image_surface(sprite_path) if sprite_path else None
        # Scale to desired size
        if surf is not None:
            surf = pygame.transform.smoothscale(surf, (base_w, base_h))
        # If sprite missing, create a colored circle surface instead
        if surf is None:
            surf = pygame.Surface((base_w, base_h), pygame.SRCALPHA)
            pygame.draw.circle(surf, (30,150,30), (base_w//2, base_h//2), base_w//2)
        w, h = surf.get_size()
        obj = {
            "id": sp["id"],
            "common_name": sp["common_name"],
            "scientific_name": sp["scientific_name"],
            "description": sp["description"],
            "habitat_info": sp["habitat_info"],
            "s_image": sp.get("s_image", ""),
            "native_status": sp.get("native_status", ""),
            "fun_fact": sp.get("fun_fact", ""),
            "x": sp["x"],
            "y": sp["y"],
            "sprite_path": sprite_path,
            "surface": surf,
            "w": w,
            "h": h,
            # runtime-only for animation
            "pulse_phase": random.random() * 3.14
        }
        _species_objects.append(obj)

    return _species_objects

# Draw sprites with pulse effect on hover
def draw_species(screen, hover_id, time_elapsed):
    """Draw sprites; apply pulse scale to hovered sprite."""
    for obj in _species_objects:
        x, y = obj["x"], obj["y"]
        surf = obj["surface"]
        base_w, base_h = obj["w"], obj["h"]
        draw_w, draw_h = base_w, base_h

        # pulse on hover
        if hover_id == obj["id"]:
            obj["pulse_phase"] += time_elapsed * 6.0  # speed
            scale = 1.0 + 0.12 * (0.5 + 0.5 * math.sin(obj["pulse_phase"]))  # 0.88..1.12 oscillation for width
            draw_w = int(base_w * scale)
            draw_h = int(base_h * scale)
            scaled = pygame.transform.smoothscale(surf, (draw_w, draw_h))
            draw_x = int(x - draw_w // 2)
            draw_y = int(y - draw_h // 2)
            screen.blit(scaled, (draw_x, draw_y))
            # outline glow
            outline_rect = pygame.Rect(draw_x-4, draw_y-4, draw_w+8, draw_h+8)
            pygame.draw.rect(screen, (255, 220, 120), outline_rect, 2, border_radius=8)
        else:
            # draw normally centered at (x,y)
            draw_x = int(x - draw_w // 2)
            draw_y = int(y - draw_h // 2)
            screen.blit(surf, (draw_x, draw_y))

# Sprite hitbox
def point_inside_sprite(px, py, obj):
    w, h = obj["w"], obj["h"]
    left = obj["x"] - w // 2
    top = obj["y"] - h // 2
    
    return left <= px <= left + w and top <= py <= top + h

# Draw tooltip near mouse
def draw_tooltip(surface, text, pos, tooltip_bg_color=(255, 255, 255)):
    font = pygame.font.SysFont(None, 18)
    rendered = font.render(text, True, (0,0,0))
    padding = 6
    w = rendered.get_width() + 2 * padding
    h = rendered.get_height() + 2 * padding
    x = pos[0] + 12
    y = pos[1] + 12
    sw, sh = surface.get_size()
    if x + w > sw: x = pos[0] - w - 12
    if y + h > sh: y = pos[1] - h - 12
    rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, tooltip_bg_color, rect, border_radius=4)
    pygame.draw.rect(surface, (0,0,0), rect, 1, border_radius=4)
    surface.blit(rendered, (x + padding, y + padding))