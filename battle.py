import monster
import random
import screen
from math import floor
from pygame import Rect
from pygame import draw

import time_keep
import sprites
import text_system

in_battle = False

BUTTON_WIDTH = 90
BUTTON_HEIGHT = 20
button_selector = 0
battle_sequence_tracker = "NONE"
select = False
is_back = False

hp_max_width = 38
hp_height = 6
player_hp_bar = None
enemy_hp_bar = None
hp_shrink = 17

dmg_calculated = False
damage = 0
initial_HP = None
accuracy_checked = False

player_turn_taken = False
enemy_turn_taken = False

hit_counter = 0

p_ability_done = False
e_ability_done = False

#STAT_CHANGES: [ATK, DEF, SPATK, SPDEF, SPD]
# [[id, exp, HP, ATK, DEF, SPATK, SPDEF, SPD, Ability, HeldItem, [[Move, pp], ...]], [STAT_CHANGES], currentHP]
player_team = []
enemy_team = []
active_monster_p = ""
active_monster_e = ""

p_selected_attack = None
e_selected_attack = None

turn_trigger_tracker = "NONE"
#START_BATTLE, START_TURN, END_TURN, BEFORE_P_ATTACKED, P_ATTACKED, BEFORE_E_ATTACKED, E_ATTACKED, P_ITEM_USED, E_ITEM_USED

player_action = "ACTION_NONE"
enemy_action = "ACTION_NONE"
move_first = "PLAYER"

battle_buttons = []
is_trainer = False
opp_name = "Opponent"

prev_battle_sequence_tracker = None

ability_started = False

def initiate_battle(pParty, eParty, trainer, traier_name = "Opponent"):
    if len(pParty) == 0 or len(eParty) == 0:
        return "invalid teams"
    else:
        global player_team
        global enemy_team
        global in_battle
        global active_monster_p
        global active_monster_e
        global turn_trigger_tracker
        global battle_sequence_tracker
        global button_selector
        global select
        global is_back
        global enemy_hp_bar
        global player_hp_bar
        global accuracy_checked
        global hit_counter
        global is_trainer
        global opp_name
        global p_ability_done
        global e_ability_done
        global ability_started

        ability_started = False
        p_ability_done = False
        e_ability_done = False

        opp_name = traier_name
        is_trainer = trainer
        accuracy_checked = False
        hit_counter = 0

        player_team = pParty
        enemy_team = eParty

        active_monster_p = player_team[0]
        active_monster_e = enemy_team[0]
        in_battle = True
        turn_trigger_tracker = "START_BATTLE"

        battle_sequence_tracker = "INITIAL_SEND_OUT"
        start_battle_message()
        
        initiate_selection_buttons()
        button_selector = 0
        select = False
        is_back = False

        sprites.initiate_sprites()
        sprites.update_battle_sprites(active_monster_p, active_monster_e)

        enemy_hp_bar = Rect((screen.SCREEN_WIDTH - 30 - hp_max_width)* screen.SCALE, 20 * screen.SCALE, hp_max_width * screen.SCALE, hp_height * screen.SCALE)
        player_hp_bar = Rect(30 * screen.SCALE, 20 * screen.SCALE, hp_max_width * screen.SCALE, hp_height * screen.SCALE)

        return "start"

def initiate_move_buttons():
    global battle_buttons
    battle_buttons.clear()
    moves = monster.get_battle_moveset(active_monster_p)
    if len(moves) >= 1:
        battle_buttons.append(Rect(25 * screen.SCALE, (screen.SCREEN_HEIGHT - 5 - BUTTON_HEIGHT - 10 - BUTTON_HEIGHT) * screen.SCALE, BUTTON_WIDTH * screen.SCALE, BUTTON_HEIGHT * screen.SCALE))
    if len(moves) >= 2:
        battle_buttons.append(Rect(screen.SCREEN_WIDTH * screen.SCALE/2 + 5 * screen.SCALE, (screen.SCREEN_HEIGHT - 5 - BUTTON_HEIGHT - 10 - BUTTON_HEIGHT) * screen.SCALE, BUTTON_WIDTH * screen.SCALE, BUTTON_HEIGHT * screen.SCALE))
    if len(moves) >= 3:
        battle_buttons.append(Rect(25 * screen.SCALE, (screen.SCREEN_HEIGHT - 10 - BUTTON_HEIGHT) * screen.SCALE, BUTTON_WIDTH * screen.SCALE, BUTTON_HEIGHT * screen.SCALE))
    if len(moves) >= 4:
        battle_buttons.append(Rect(screen.SCREEN_WIDTH * screen.SCALE/2 + 5 * screen.SCALE, (screen.SCREEN_HEIGHT - 10 - BUTTON_HEIGHT) * screen.SCALE, BUTTON_WIDTH * screen.SCALE, BUTTON_HEIGHT * screen.SCALE))

def initiate_selection_buttons():
    global battle_buttons
    battle_buttons.clear()

    battle_buttons.append(Rect(25 * screen.SCALE, (screen.SCREEN_HEIGHT - 5 - BUTTON_HEIGHT - 10 - BUTTON_HEIGHT) * screen.SCALE, BUTTON_WIDTH * screen.SCALE, BUTTON_HEIGHT * screen.SCALE))
    battle_buttons.append(Rect(screen.SCREEN_WIDTH * screen.SCALE/2 + 5 * screen.SCALE, (screen.SCREEN_HEIGHT - 5 - BUTTON_HEIGHT - 10 - BUTTON_HEIGHT) * screen.SCALE, BUTTON_WIDTH * screen.SCALE, BUTTON_HEIGHT * screen.SCALE))
    battle_buttons.append(Rect(25 * screen.SCALE, (screen.SCREEN_HEIGHT - 10 - BUTTON_HEIGHT) * screen.SCALE, BUTTON_WIDTH * screen.SCALE, BUTTON_HEIGHT * screen.SCALE))
    battle_buttons.append(Rect(screen.SCREEN_WIDTH * screen.SCALE/2 + 5 * screen.SCALE, (screen.SCREEN_HEIGHT - 10 - BUTTON_HEIGHT) * screen.SCALE, BUTTON_WIDTH * screen.SCALE, BUTTON_HEIGHT * screen.SCALE))

def determine_turn_order():
    global move_first

    if player_action == "ITEM" or  player_action == "RUN" or player_action == "SWITCH":
        move_first = "PLAYER"
    elif enemy_action == "ITEM" or enemy_action == "SWITCH":
        move_first = "ENEMY"
    elif monster.get_move_priority(p_selected_attack[0]) > monster.get_move_priority(e_selected_attack[0]):
        move_first = "PLAYER"
    elif monster.get_move_priority(e_selected_attack[0]) > monster.get_move_priority(p_selected_attack[0]):
        move_first = "ENEMY"
    elif monster.get_battle_SPD(active_monster_p) > monster.get_battle_SPD(active_monster_e):
        move_first = "PLAYER"
    elif monster.get_battle_SPD(active_monster_p) < monster.get_battle_SPD(active_monster_e):
        move_first = "ENEMY"
    else:
        if random.random() < 0.5:
            move_first = "PLAYER"
        else:
            move_first = "ENEMY"

#Attacker, Defender, Move used
def calculate_damage(battle_mon1, battle_mon2, move_name):
    global damage

    ATK = None
    DEF = None
    move_dmg = None
    BOOST_ATK = None
    BOOST_DEF = None
    if(monster.get_move_phys_spec(move_name) == "PHYSICAL"):
        ATK = monster.get_battle_ATK(battle_mon1)
        DEF = monster.get_battle_DEF(battle_mon2)
        BOOST_ATK = monster.get_battle_ATK_BOOST(battle_mon1) * 1.5
        BOOST_DEF = monster.get_battle_DEF_BOOST(battle_mon2) * 1.5
    else:
        ATK = monster.get_battle_SPATK(battle_mon1)
        DEF = monster.get_battle_SPDEF(battle_mon2)
        BOOST_ATK = monster.get_battle_SPATK_BOOST(battle_mon1) * 1.5
        BOOST_DEF = monster.get_battle_SPDEF_BOOST(battle_mon2) * 1.5

    if BOOST_ATK == 0:
        BOOST_ATK = 1
    if BOOST_DEF == 0:
        BOOST_DEF = 1
    move_dmg = monster.get_move_dmg(move_name)
    type_efctv = monster.get_type_effectiveness(monster.get_move_type(move_name), monster.get_battle_type(battle_mon2))
    ability_boost = 1

    damage = floor((ATK/DEF) * (move_dmg/8) * type_efctv * ability_boost * BOOST_ATK / BOOST_DEF * ability_boost * monster.calculate_level_from_exp(battle_mon1[1]) / monster.calculate_level_from_exp(battle_mon2[1]) * 2)
        
def get_buttons():
    return battle_buttons

def draw_battle_button(window):
    for idx, button in enumerate(battle_buttons):
        if idx == button_selector:
            window.blit(sprites.button_on_sprite, (button.x, button.y))
        else:
            window.blit(sprites.button_off_sprite, (button.x, button.y))

def draw_HP_bars(window):
    draw.rect(window, (0, 255, 0), player_hp_bar)
    draw.rect(window, (0, 255, 0), enemy_hp_bar)

def draw_mons(window):
    
    if sprites.sprite_mode == "SINGLE":
        window.blit(sprites.player_mon_sprite, (15 * screen.SCALE, 35 * screen.SCALE))
        window.blit(sprites.enemy_mon_sprite, ((screen.SCREEN_WIDTH - 15 - 64) * screen.SCALE, 35 * screen.SCALE))
    elif sprites.sprite_mode == "BACK":
        window.blit(sprites.player_mon_sprite, (15 * screen.SCALE, 50 * screen.SCALE))
        window.blit(sprites.enemy_mon_sprite, ((screen.SCREEN_WIDTH - 15 - 64) * screen.SCALE, 25 * screen.SCALE))

def draw_back_box(window):
    window.blit(sprites.text_box_sprite, (0, (screen.SCREEN_HEIGHT - 65) * screen.SCALE))

def update_button_counter(amount):
    global button_selector

    original_selector = button_selector

    if amount == 1 and button_selector % 2 != 0:
        amount = -1
    elif amount == -1 and button_selector % 2 == 0:
        amount = 1
    button_selector += amount
    if button_selector < 0:
        button_selector = 4 + button_selector
    button_selector = button_selector % 4

    if button_selector < 0 or button_selector > len(battle_buttons) - 1:
        button_selector = original_selector

def battle_main():
    global select
    global is_back
    global battle_sequence_tracker
    global move_first
    global active_monster_e
    global active_monster_p
    global hit_counter
    global prev_battle_sequence_tracker
    global ability_started

    if battle_sequence_tracker == "INITIAL_SEND_OUT":
        if text_system.displaying_text == False:
            if p_ability_done == False and e_ability_done == False and check_abilities():
                set_abil_vars()
                prev_battle_sequence_tracker = battle_sequence_tracker
                battle_sequence_tracker = "ABILITY_ACTIVATE"
            else:
                battle_sequence_tracker = "ACTION_SELECT"
    elif battle_sequence_tracker == "ACTIVATE_ABILITY":
        if p_ability_done == False:
            pass
        elif e_ability_done == False:
            pass
        else:
            pass
    elif battle_sequence_tracker == "ACTION_SELECT":
        check_action_select()
    elif battle_sequence_tracker =="ATTACK_SELECT":
        check_attack_select()
    elif battle_sequence_tracker == "ATTACK_SEQUENCE_BEGIN":
        determine_enemy_action()
        determine_turn_order()
        display_atk_seq_text_box(move_first)

        battle_sequence_tracker = "TEXT_BOX_FIRST"
    elif battle_sequence_tracker == "TEXT_BOX_FIRST":
        if text_system.displaying_text == False:
            battle_sequence_tracker = "ANIMATION"
            if get_move_first_action(move_first) == "ATTACK":
                if check_accuracy(get_move_first_move(move_first)) == False:
                    battle_sequence_tracker = "MISSED"
                    if move_first == "PLAYER":
                        text_system.display_text(["Your " + monster.monster_list[active_monster_p[0]][0] + "'s attack missed."])
                    else:
                        text_system.display_text(["The opponent " + monster.monster_list[active_monster_p[0]][0] + "'s attack missed."])
    elif battle_sequence_tracker == "ANIMATION":
        if True:
            battle_sequence_tracker = "HP_BAR"
    elif battle_sequence_tracker == "MISSED":
        if text_system.displaying_text == False:
            hit_counter = monster.get_move_max_hits(get_move_first_move(move_first)[0]) + 1
            battle_sequence_tracker = "CHECK_END_TURN"
    elif battle_sequence_tracker == "HP_BAR":
        if get_move_first_action(move_first) == "ATTACK":
            global dmg_calculated
            if dmg_calculated == False:
                global damage
                global initial_HP
                
                hit_counter += 1
                if move_first == "PLAYER":
                    calculate_damage(active_monster_p, active_monster_e, p_selected_attack[0])
                    initial_HP = monster.get_battle_current_HP(active_monster_e)
                    active_monster_e = monster.damage_battle_mon(active_monster_e, damage)
                    print("PLAYER")
                else:
                    calculate_damage(active_monster_e, active_monster_p, e_selected_attack[0])
                    initial_HP = monster.get_battle_current_HP(active_monster_p)
                    active_monster_p = monster.damage_battle_mon(active_monster_p, damage)
                    print("ENEMY")
                dmg_calculated = True
                if damage > initial_HP:
                    damage = initial_HP
            if move_first == "PLAYER":
                global enemy_hp_bar
                shrink_off_set = time_keep.delta_time() / hp_shrink

                if enemy_hp_bar.width - shrink_off_set < (initial_HP - damage) / monster.get_battle_HP(active_monster_e) * hp_max_width * screen.SCALE:
                    enemy_hp_bar = Rect((screen.SCREEN_WIDTH - 30 - hp_max_width)* screen.SCALE, 20 * screen.SCALE, (initial_HP - damage) / monster.get_battle_HP(active_monster_e) * hp_max_width * screen.SCALE, hp_height * screen.SCALE)
                    battle_sequence_tracker = "CHECK_END_TURN"
                    if monster.get_type_effectiveness(monster.get_move_type(p_selected_attack[0]), monster.get_battle_type(active_monster_e)) > 1:
                        text_system.display_text(["It was super effective!"])
                        battle_sequence_tracker = "CHECK_EFFECTIVE"
                    elif monster.get_type_effectiveness(monster.get_move_type(p_selected_attack[0]), monster.get_battle_type(active_monster_e)) < 1:
                        text_system.display_text(["It wasn't very effective."])
                        battle_sequence_tracker = "CHECK_EFFECTIVE"
                    elif monster.get_battle_current_HP(active_monster_e) <= 0:
                        battle_sequence_tracker = "FAINT"
                        text_system.display_text(["The opponent's " + monster.monster_list[active_monster_e[0]][0] + " fainted."])
                else:
                    enemy_hp_bar.width -= shrink_off_set
            else:
                global player_hp_bar
                shrink_off_set = time_keep.delta_time() / hp_shrink

                if player_hp_bar.width - shrink_off_set < (initial_HP - damage) / monster.get_battle_HP(active_monster_p) * hp_max_width * screen.SCALE:
                    player_hp_bar = Rect(30 * screen.SCALE, 20 * screen.SCALE, (initial_HP - damage) / monster.get_battle_HP(active_monster_p) * hp_max_width * screen.SCALE, hp_height * screen.SCALE)
                    battle_sequence_tracker = "CHECK_END_TURN"
                    if monster.get_type_effectiveness(monster.get_move_type(e_selected_attack[0]), monster.get_battle_type(active_monster_p)) > 1:
                        text_system.display_text(["It was super effective!"])
                        battle_sequence_tracker = "CHECK_EFFECTIVE"
                    elif monster.get_type_effectiveness(monster.get_move_type(e_selected_attack[0]), monster.get_battle_type(active_monster_p)) < 1:
                        text_system.display_text(["It wasn't very effective."])
                        battle_sequence_tracker = "CHECK_EFFECTIVE"
                    elif monster.get_battle_current_HP(active_monster_p) <= 0:
                        battle_sequence_tracker = "FAINT"
                        text_system.display_text(["Your " + monster.monster_list[active_monster_p[0]][0] + " fainted."])
                else:
                    player_hp_bar.width -= shrink_off_set
    elif battle_sequence_tracker == "FAINT":
        if text_system.display_text == False:
            pass
    elif battle_sequence_tracker == "CHECK_EFFECTIVE":
        if text_system.displaying_text == False:
            battle_sequence_tracker = "CHECK_END_TURN"

            if move_first == "PLAYER":
                if monster.get_battle_current_HP(active_monster_e) <= 0:
                    text_system.display_text(["The opponent's " + monster.monster_list[active_monster_e[0]][0] + " fainted."])
                    battle_sequence_tracker = "FAINT"
            else:
                if monster.get_battle_current_HP(active_monster_p) <= 0:
                    text_system.display_text(["Your " + monster.monster_list[active_monster_e[0]][0] + " fainted."])
                    battle_sequence_tracker = "FAINT"

    elif battle_sequence_tracker == "CHECK_END_TURN":
        global player_turn_taken
        global enemy_turn_taken

        if monster.get_move_max_hits(get_move_first_move(move_first)[0]) > hit_counter:
            if check_accuracy(get_move_first_move(move_first)) == False:
                    if hit_counter == 1:
                        text_system.display_text(["It hit " + str(hit_counter) + " time."])
                    else:
                        text_system.display_text(["It hit " + str(hit_counter) + " times."])
                    battle_sequence_tracker = "MISSED"
            else:
                battle_sequence_tracker = "ANIMATION"
        elif monster.get_move_max_hits(get_move_first_move(move_first)[0]) == hit_counter and hit_counter != 1:
            text_system.display_text(["It hit " + str(hit_counter) + " times."])
            hit_counter += 1
            battle_sequence_tracker = "MISSED"
        elif move_first == "PLAYER":
            player_turn_taken = True
            hit_counter = 0
        elif move_first == "ENEMY":
            enemy_turn_taken = True
            hit_counter = 0
        if player_turn_taken and enemy_turn_taken:
            battle_sequence_tracker = "ACTION_SELECT"
            player_turn_taken = False
            enemy_turn_taken = False
            initiate_selection_buttons()
        else:
            if battle_sequence_tracker != "MISSED" and battle_sequence_tracker != "ANIMATION":
                if player_turn_taken:
                    move_first = "ENEMY"
                    display_atk_seq_text_box(move_first)
                    battle_sequence_tracker = "TEXT_BOX_FIRST"
                else: 
                    move_first = "PLAYER"
                    display_atk_seq_text_box(move_first)
                    battle_sequence_tracker = "TEXT_BOX_FIRST"     
        reset_turn()
            

    check_back()

    select = False
    is_back = False

def select_button():
    global select
    select = True

def check_action_select():
    global button_selector
    global battle_sequence_tracker
    global select
    if select == True:
        if button_selector == 0:
            print("switching to ATTACK_SELECT")
            battle_sequence_tracker = "ATTACK_SELECT"
            initiate_move_buttons()
            select = False
        elif button_selector == 1:
            battle_sequence_tracker = "ITEM_SELECT"
            select = False
        elif button_selector == 2:
            battle_sequence_tracker = "PARTY_VIEW"
            select = False
        elif button_selector == 3:
            battle_sequence_tracker = "ATTEMPT_RUN"
            select = False
    select = False

def check_attack_select():
    global button_selector
    global battle_sequence_tracker
    global select
    global p_selected_attack
    global player_action

    if select == True:
        p_selected_attack = monster.get_battle_moveset(active_monster_p)[button_selector]
        battle_sequence_tracker = "ATTACK_SEQUENCE_BEGIN"
        player_action = "ATTACK"

def back():
    global is_back
    is_back = True

def check_back():
    global is_back
    global battle_sequence_tracker

    if battle_sequence_tracker == "ATTACK_SELECT" or battle_sequence_tracker == "ITEM_SELECT" or battle_sequence_tracker == "PARTY_VIEW" or battle_sequence_tracker == "ATTEMPT_RUN":
        if is_back:
            initiate_selection_buttons()
            battle_sequence_tracker = "ACTION_SELECT"
            is_back = False
    else:
        is_back = False

def determine_enemy_action():
    global enemy_action
    global e_selected_attack

    enemy_action = "ATTACK"
    e_selected_attack = monster.get_battle_moveset(active_monster_e)[2]

def display_atk_seq_text_box(mover):
    global move_first
    if mover == "PLAYER":
        if player_action == "ATTACK":
            text_system.display_text([monster.monster_list[active_monster_p[0]][0] + " used " + p_selected_attack[0] + "!"])
    elif mover == "ENEMY":
        if enemy_action == "ATTACK":
            text_system.display_text([monster.monster_list[active_monster_e[0]][0] + " used " + e_selected_attack[0] + "!"])

def get_move_first_action(move_first):
    if move_first == "PLAYER":
        return player_action
    else:
        return enemy_action

def reset_turn():
    global initial_HP
    global damage
    global dmg_calculated
    global accuracy_checked
    global hit_counter

    #hit_counter = 0
    accuracy_checked = False
    initial_HP = None
    damage = 0
    dmg_calculated = False

def check_accuracy(move):
    acc = monster.get_move_accuracy(move[0]) / 100
    return random.random() < acc

def get_move_first_move(move_first):
    if move_first == "PLAYER":
        return p_selected_attack
    else:
        return e_selected_attack

def start_battle_message():
    if is_trainer:
        text_system.display_text(["You are challenged by trainer " + opp_name + ".", "You sent out " + monster.monster_list[active_monster_p[0]][0] + "!", opp_name + " sent out " + monster.monster_list[active_monster_e[0]][0]])
    else:
        text_system.display_text(["A wild " + monster.monster_list[active_monster_e[0]][0] + " appeared!", "You sent out " + monster.monster_list[active_monster_p[0]][0] + "!"])

def check_ability(creature):
    return turn_trigger_tracker in monster.get_battle_ability_conditions(creature)

def check_abilities():
    return check_ability(active_monster_p) or check_ability(active_monster_e)

def activate_ability():
    pass

def set_abil_vars():
    global p_ability_done
    global e_ability_done
    global ability_started
    if check_ability(active_monster_p):
        p_ability_done = False
    else:
        p_ability_done = True
    if check_ability(active_monster_e):
        e_ability_done = False
    else:
        e_ability_done = True
    ability_started = False