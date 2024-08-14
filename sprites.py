from pygame import transform
from pygame import Surface
from pygame import image
import screen

text_box_sprite = None
button_off_sprite = None
button_on_sprite = None
box_sprite_sheet = None

player_mon_sprite = None
enemy_mon_sprite = None

sprite_mode = "SINGLE"

def initiate_sprites():
    global box_sprite_sheet
    global button_on_sprite
    global button_off_sprite
    global text_box_sprite
    
    box_sprite_sheet = image.load("Graphics/Battle_Box_Style/Default.png").convert_alpha()
    text_box_sprite = get_image(box_sprite_sheet, 0, 0, 240, 65)
    button_off_sprite = get_image(box_sprite_sheet, 0, 65, 90, 20)
    button_on_sprite = get_image(box_sprite_sheet, 90, 65, 90, 20)

def get_image(sheet, x, y, width, height):
    img = Surface((width, height)).convert_alpha()
    img.blit(sheet, (0, 0), (x, y, width, height))
    img = transform.scale(img, (width * screen.SCALE, height * screen.SCALE))
    return img

def update_battle_sprites(p_mon, e_mon):
    global player_mon_sprite
    global enemy_mon_sprite

    player_mon_sprite = image.load("Graphics/Battle_Sprites/" + str(p_mon[0]) + ".png").convert_alpha()
    enemy_mon_sprite = image.load("Graphics/Battle_Sprites/" + str(e_mon[0]) + ".png").convert_alpha()
    player_mon_sprite = transform.scale(player_mon_sprite, (64 * screen.SCALE, 64 * screen.SCALE))
    enemy_mon_sprite = transform.scale(enemy_mon_sprite, (64 * screen.SCALE, 64 * screen.SCALE))

    if sprite_mode == "SINGLE":
            player_mon_sprite = transform.flip(player_mon_sprite, True, False)