import random
from math import cbrt

#monster list structure (name followed by base stats): ["name:, [type1, type2], health, attack, defense, special attack, special defense, speed]
monster_list = {0 : ["MONSTER_NONE", ["Normal"], 100, 150, 200, 233, 290, 120],
                }



learnset_list = {0 : {1 : "TEST_MOVE",
                      2 : "TEST_MOVE_2",
                      3 : "TEST_MOVE_3",
                },
           }

#key = name, value = [damage, %accuracy, "type", [effect], priority, pp, special/physical, num_hits]
valid_moves = {"TEST_MOVE" : [1, 70, "Normal", [], 0, 10, "PHYSICAL", 3],
               "TEST_MOVE_2" : [20, 95, "Normal", [], 1, 20, "SPECIAL", 1],
               "TEST_MOVE_3" : [50, 100, "Normal", [], 2, 1, "PHYSICAL", 1],
               }

#output: is weak against, is strong against, has no effect
valid_types = {"Normal" : [["Normal"], [], []],
               }

#[trigger, effect, counter/severity/extra (0 if none)] -> [severity, turn_counter, [STAT or other]]
#triggers: START_BATTLE, START_TURN, END_TURN, BEFORE_ATTACK, AFTER_ATTACK, BEFORE_ATTACKED, AFTER_ATTACKED, ITEM_USED, ON_SWITCH

valid_abilities = {"TEST_ABILITY" : [["START_TURN", "START_BATTLE"], "RAISE_ATTACK_1"], }

possible_abilities = {0 : ["TEST_ABILITY"], }

possible_effects = {"RAISE_ATTACK_1" : {"type" : "BOOST_STAT",
                                        "stages" : 1,
                                         "chance" : 100,
                                         "target" : "USER"}}

def add_mon(name, type_list, HP, ATK, DEF, SPATK, SPDEF, SPD, possible_abilities):
    if type(name) is not str:
        return "Invalid name"
    if type(type_list) is not list:
        return "invalid type/s"
    for t in type_list:
        if not is_valid_type(t):
            return "invalid type/s"
    if type(HP) is not int:
        return "Invalid HP stat"
    if type(ATK) is not int:
        return "invalid Attack stat"
    if type(DEF) is not int:
        return "invalid Defense stat"
    if type(SPATK) is not int:
        return "invalid Special Attack stat"
    if type(SPDEF) is not int:
        return "invalid Special Defense stat"
    if type(SPD) is not int:
        return "invalid Speed stat"
    if type(possible_abilities) is not list:
        return "invalid ability list"
    
    id = len(monster_list)
    monster_list[id] = [name, HP, ATK, DEF, SPATK, SPDEF, SPD]
    valid_abilities[id] = possible_abilities
    add_learnset(id, [[1, "TEST_MOVE"]])
    return id

#moves is structured [[learn_level, name of move] , [...], ...]
def add_learnset(id, moves):
    new_learnset = dict()

    for item in moves:
        if(is_valid_move(item[1])):
            new_learnset[item[0]] = item[1]

    global learnset_list
    learnset_list[id] = new_learnset

def add_new_move(name, damage, accuracy, type_mon, effect, priority, pp, physical):
    if type(damage) is not int:
        return "invalid damage"
    if type(accuracy) is not int:
        return "invalid accuracy"
    if is_valid_type(type_mon) == False:
        return "invalid type"
    if type(effect) is not list:
        return "invalid effects"
    if type(priority) is not int:
        return "invalid priority"
    if type(pp) is not int:
        return "invalid pp"
    if physical != "PHYSICAL" or physical != "SPECIAL" or physical != "NONE":
        return "invalid move physical/special designation"
    
    valid_moves[str(name)] = [damage, accuracy, type_mon, effect, priority, pp, physical]
    return "move added"

def add_new_type(name, weak, strong, no_effect):
    if name in valid_types:
        return "type already exists"
    valid_types[name] = [weak, strong, no_effect]

#input string
def is_valid_move(move):
    return move in valid_moves

def is_valid_type(mon_type):
    return type(mon_type) == str and mon_type in valid_types

def get_battle_type(monster):
    return monster_list[monster[0]][1]

def get_battle_HP(monster):
    return monster[2]

def get_battle_ATK(monster):
    return monster[3]

def get_battle_DEF(monster):
    return monster[4]

def get_battle_SPATK(monster):
    return monster[5]

def get_battle_SPDEF(monster):
    return monster[6]

def get_battle_SPD(monster):
    return monster[7]

def get_battle_ability(monster):
    return monster[8]

def get_battle_ability_conditions(monster):
    return valid_abilities[get_battle_ability(monster)][0]

def get_ability_effect(ability):
    return valid_abilities[ability][1]

def get_battle_item(monster):
    return monster[9]

def get_battle_moveset(monster):
    return monster[10]

def get_battle_ATK_BOOST(monster):
    return monster[11][0]

def get_battle_DEF_BOOST(monster):
    return monster[11][1]

def get_battle_SPATK_BOOST(monster):
    return monster[11][2]

def get_battle_SPDEF_BOOST(monster):
    return monster[11][3]

def get_battle_SPD_BOOST(monster):
    return monster[11][4]

def get_battle_current_HP(monster):
    return monster[12]

def get_move_dmg(move):
    if(is_valid_move(move)):
        return valid_moves[move][0]
    
def get_move_accuracy(move):
    if(is_valid_move(move)):
        return valid_moves[move][1]

def get_move_type(move):
    if(is_valid_move(move)):
        return valid_moves[move][2]
    
def get_move_effect(move):
    if(is_valid_move(move)):
        return valid_moves[move][3]
    
def get_move_priority(move):
    if(is_valid_move(move)):
        return valid_moves[move][4]
    
def get_move_max_pp(move):
    if(is_valid_move(move)):
        return valid_moves[move][5]
    
def get_move_phys_spec(move):
    if(is_valid_move(move)):
        return valid_moves[move][6]
    
def get_move_max_hits(move):
    return valid_moves[move][7]

def get_type_effectiveness(move_type, mon_type):
    multiplier = 1
    if(is_valid_type(move_type) == False):
        return "invalid type"
    for type in mon_type:
        if(is_valid_type(type) == False):
            return "invalid type"
        if move_type in valid_types[type][2]:
            return 0
        elif move_type in valid_types[type][0]:
            multiplier = multiplier * 1.5
        elif move_type in valid_types[type][1]:
            multiplier = multiplier / 1.5

    return multiplier

#team is a list
def give_battle_mon(team, mon):
    if(len(team) >= 6):
        return "team full"
    else:
        team.append(mon)
    return team

#to pass in a moveset, structure like []
#[id, exp, HP, ATK, DEF, SPATK, SPDEF, SPD, Ability, HeldItem, [[Move, pp], ...]], [STAT_CHANGES], currentHP
def generate_battle_mon(mon_id, lvl=1, moveset="NONE", ability="ANY"):
    if mon_id not in monster_list:
        return "Monster does not exist"
    else:
        stat_list = calculate_stats_from_level(mon_id, lvl)
        exp = calculate_exp_from_lvl(lvl)
        held_item = None
        stat_changes = [0, 0, 0, 0, 0]
        if ability not in valid_abilities:
            ability_list = possible_abilities[mon_id]
            ability = random.choice(ability_list)
        if moveset == "NONE":
            moveset = create_moveset(mon_id, lvl)
        return [mon_id, exp, stat_list[0], stat_list[1], stat_list[2], stat_list[3], stat_list[4], stat_list[5], ability, held_item, moveset, stat_changes, stat_list[0]]

def get_base_stats(mon_id):
    if (mon_id not in monster_list):
        return "invalid monster id"

    mon_stats = []
    #HP, ATK, DEF, SPATK, SPDEF, SPD
    mon_stats.append(monster_list[mon_id][2])
    mon_stats.append(monster_list[mon_id][3])
    mon_stats.append(monster_list[mon_id][4])
    mon_stats.append(monster_list[mon_id][5])
    mon_stats.append(monster_list[mon_id][6])
    mon_stats.append(monster_list[mon_id][7])
    return mon_stats

def calculate_stats_from_level(mon_id, level):
    if mon_id not in monster_list:
        return "invalid monster id"
    if level < 1 or level > 100:
        return "invalid level"
    
    base_stats = get_base_stats(mon_id)
    stats = []
    percentage = float(level) / 100

    stats.append(base_stats[0] * percentage + 20)
    stats.append(base_stats[1] * percentage + 4)
    stats.append(base_stats[2] * percentage + 4)
    stats.append(base_stats[3] * percentage + 4)
    stats.append(base_stats[4] * percentage + 4)
    stats.append(base_stats[5] * percentage + 4)

    for idx, stat in enumerate(stats):
        if stat <= 1:
            stats[idx] = 1
    
    return stats

#exp = level^3
#level = cube root of exp
def calculate_level_from_exp(exp):
    return int(cbrt(exp))

def calculate_exp_from_lvl(lvl):
    return int(lvl * lvl * lvl)

def give_exp(monster, amount):
    monster[1] += amount
    return monster

def create_moveset(mon_id, lvl):
    counter = 0
    moves = []
    for key, value in learnset_list[mon_id].items():
        if key > lvl:
            return moves
        else:
            if len(moves) < 4:
                moves.append([value, valid_moves[value][5]])
            else:
                moves[counter] = [value, valid_moves[value][5]]
                counter += counter
    return moves

def damage_battle_mon(monster, amount):
    monster[12] -= amount
    return monster