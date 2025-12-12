import os
import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN

from load_helpers import load_species_from_csv, load_image_surface
from popup import wrap_text, open_popup, close_popup, draw_popup, handle_popup_click, get_popup_state
from sprites import prepare_species_objects, draw_species, point_inside_sprite, draw_tooltip, _species_objects
from home_button import draw_home_button, handle_home_button_click
from welcome_screen import draw_welcome_screen, handle_welcome_click
from mute_button import draw_mute_button, handle_mute_button_click


def run_app():

    background_image = r"data\game_background.png"
    species_csv = r"data/display_tank_species_data.csv"

    global _game_state, is_muted
    screen_width = 1080
    screen_height = 720
    fps = 60
    species_default_size = (160, 180)  # base sprite size (width, height)
    text_color = (30, 30, 30)   # dark grey
    popup_width = 700
    popup_height = 550
    popup_border_color = (100, 100, 100)   # grey
    popup_bg_color = (220, 220, 220)
    
    _game_state = "welcome"  # starts off on welcome screen
    _start_button_rect = None  # stores the start button rect for click detection
    _home_button_rect = None  # stores the home button rect on game screen for click detection
    _mute_button_rect = None  # stores the mute button rect for click detection
    is_muted = False # tracks whether music is muted

    # Ensure species csv exist 
    if not os.path.exists(species_csv):
        print("Missing species CSV:", species_csv)
        return
    # Ensure background image exists
    if not os.path.exists(background_image):
        print("Warning: background image not found at", background_image)
        print("Put a background image there or change background_image variable in the script.")

    # Initialize Pygame env
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Display_Tank_Explorer")
    pygame.mixer.music.load(r"data\ES_Ocean Air - Aerian.mp3")
    pygame.mixer.music.play(-1) # loop indefinitely
    clock = pygame.time.Clock()

    # Gets list of species from CSV and prepare sprite objects
    prepare_species_objects(species_csv, species_default_size)

    # load background surface
    background_surf = None
    if os.path.exists(background_image):
        try:
            background_surf = load_image_surface(background_image)
            if background_surf:
                background_surf = pygame.transform.smoothscale(background_surf, (screen_width, screen_height))
        except Exception as e:
            print("Failed to load background:", e)

    hover_id = None
    running = True
    last_time = pygame.time.get_ticks() / 1000.0

    while running:
        current_time = pygame.time.get_ticks() / 1000.0
        dt = current_time - last_time
        last_time = current_time

        for event in pygame.event.get():
            # Esc key to quit
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                if _game_state == "main":
                    if get_popup_state():
                        close_popup()
                    else:
                        _game_state = "welcome"
                else:
                    running = False
            
            # Actions on mouse click
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                
                if _game_state == "welcome":
                    action, new_mute = handle_welcome_click((mx, my), is_muted)
                    if action == "mute":
                        is_muted = new_mute
                    elif action == "start":
                        _game_state = "main"
                elif _game_state == "main":
                    # Check mute button first
                    mute_result = handle_mute_button_click((mx, my), is_muted)
                    if mute_result is not None:
                        is_muted = mute_result
                    # Check home button
                    if handle_home_button_click((mx, my)):
                        _game_state = "welcome"
                        close_popup()
                    # If popup open, closes popup when clicked outside popup or closed
                    elif get_popup_state():
                        result = handle_popup_click((mx, my), screen_width, screen_height, popup_width, popup_height, get_popup_state())
                        if result == "close":
                            close_popup()
                    else:
                        # Sprite clicked, popup open
                        for obj in _species_objects:
                            if point_inside_sprite(mx, my, obj):
                                open_popup(obj)
                                break

        if _game_state == "welcome":
            # Welcome screen
            draw_welcome_screen(screen, screen_width, screen_height, is_muted)
        else:
            # Main game screen
            mx, my = pygame.mouse.get_pos()

            # Only detect hover if no popup open
            # Hover gives common species name
            if not get_popup_state(): 
                new_hover = None
                for obj in reversed(_species_objects):
                    if point_inside_sprite(mx, my, obj):
                        new_hover = obj["id"]
                        break
                hover_id = new_hover
            else:
                hover_id = None

            # Background
            if background_surf:
                screen.blit(background_surf, (0,0))
            else:
                screen.fill((170,214,170))

            # Draw sprites with hover pulse
            draw_species(screen, hover_id, dt)

            # tooltip for hover feature
            if hover_id:
                name = next((o["common_name"] for o in _species_objects if o["id"] == hover_id), "")
                draw_tooltip(screen, name, (mx, my))
            
            # Buttons on game screen
            draw_home_button(screen)
            draw_mute_button(screen, screen_width, is_muted)
            
            # Draw popup if sprite clicked
            draw_popup(screen, screen_width, screen_height, popup_width, popup_height, popup_border_color, popup_bg_color, text_color, get_popup_state())

        pygame.display.flip()
        clock.tick(fps) # Control frame rate

    pygame.mixer.music.stop()
    pygame.quit()
