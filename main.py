import pygame
from pygame.locals import *

import pygame.freetype

import monster
import battle
import screen as display_screen
import text_system
import time_keep
import sprites

is_running = False
player = pygame.Rect((0, 0, 16, 24))

is_in_battle = False
is_in_overworld = False
is_in_menu = False
is_in_start = False

battle_buttons = []

# [id, exp, HP, ATK, DEF, SPATK, SPDEF, SPD, Ability, HeldItem, [[Move, pp], ...]], [STAT_CHANGES]]
player_team = []
enemy_team = []

def main():

    pygame.init()
    screen = display_screen.get_screen()
    global is_running
    global player_team
    global enemy_team
    global battle_buttons

    is_running = True
    text_system.initialize_font(screen, display_screen.SCALE)
    sprites.initiate_sprites()

    player_team = monster.give_battle_mon(player_team, monster.generate_battle_mon(0, 10))
    enemy_team = monster.give_battle_mon(enemy_team, monster.generate_battle_mon(0, 10))
    battle.initiate_battle(player_team, enemy_team, True, "Youngter Joey")
    determine_state()

    while is_running:

        time_keep.tick()

        draw_to_screen(screen)
        check_inputs()
        check_events()

        battle.battle_main()
        text_system.text_main()
        
        pygame.display.update()
        pygame.display.flip()

    pygame.quit()


def draw_to_screen(screen):
    screen.fill((0, 0, 0))

    if is_in_battle:
        battle.draw_mons(screen)
        battle.draw_back_box(screen)
        if battle.battle_sequence_tracker == "ACTION_SELECT" or battle.battle_sequence_tracker == "ATTACK_SELECT":
            battle.draw_battle_button(screen)

        battle.draw_HP_bars(screen)
    
    if text_system.displaying_text:
        battle.draw_back_box(screen)
        text_system.render_text()

def check_inputs():
    pass

def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global is_running
            is_running = False
        if event.type == pygame.KEYDOWN:
            if is_in_battle:
                if event.key == pygame.K_LEFT:
                    battle.update_button_counter(-1)
                elif event.key == pygame.K_RIGHT:
                    battle.update_button_counter(1)
                elif event.key == pygame.K_UP:
                    battle.update_button_counter(-2)
                elif event.key == pygame.K_DOWN:
                    battle.update_button_counter(2)
                elif event.key == pygame.K_RETURN:
                    battle.select_button()
                elif event.key == pygame.K_BACKSPACE:
                    battle.back()
                    print("back")
            if text_system.displaying_text:
                if event.key == pygame.K_RETURN:
                    text_system.select_enter()

def determine_state():
    global is_in_battle
    global is_in_menu
    global is_in_overworld
    global is_in_start
    if battle.in_battle:
        is_in_battle = True
        is_in_menu = False
        is_in_overworld = False
        is_in_start = False

if __name__ == "__main__":
    main()