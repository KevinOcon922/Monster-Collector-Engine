from time import sleep
import pygame.freetype

#escape character: @ followed by indicator
#@b - new box
#@s - same box
#@l - slow speed
GAME_FONT = None

text_to_show = ""
text_shown = ""
all_text = [""]
displaying_text = False
fully_displayed = False

current_line = 0
stop_inds = [0, 0, 0, 0, 0, 0]

screen = None
scale = 1
font_size = 9
current_box = 0
delay = 0.05

select = False

#[box, box, ...]
def display_text(words):
    global text_shown
    global text_to_show
    global displaying_text
    global fully_displayed
    global current_line
    global current_box
    global stop_inds
    global all_text

    stop_inds = [0, 0, 0, 0, 0, 0]
    current_box = 0
    current_line = 0
    text_shown = ""
    text_to_show = words[current_box]
    all_text = words
    displaying_text = True
    fully_displayed = False

def text_main():
    global fully_displayed
    global text_shown
    global text_to_show
    global displaying_text
    global stop_inds
    global current_line
    global all_text
    global select
    global delay

    if displaying_text:
        if text_shown != text_to_show:
            if " " in text_to_show[len(text_shown) : len(text_to_show)] and text_to_show[len(text_shown)] != " ":
                new_wrd = text_to_show[len(text_shown) : text_to_show.find(" ", len(text_shown), len(text_to_show))]

                len_new_line = 0
                if current_line == 0:
                    len_new_line = stop_inds[0] + len(new_wrd)
                else:
                    len_new_line = stop_inds[current_line] - stop_inds[current_line - 1] + len(new_wrd)
                
                if len_new_line > 50:
                    current_line += 1

            text_shown += text_to_show[len(text_shown)]

            for i in range(current_line, 6):
                stop_inds[i] += 1

            sleep(delay)
        else:
            fully_displayed = True

        if select:
            if fully_displayed:
                if current_box < len(all_text) - 1:
                    advance_box()
                else:
                    displaying_text = False
            else:
                select = False
                while text_to_show != text_shown:
                    delay = 0
                    text_main()
                delay = 0.05
            select = False

def advance_box():
    global current_box
    global text_to_show
    global text_shown
    global current_line
    global stop_inds
    global fully_displayed

    current_box += 1
    text_to_show = all_text[current_box]
    text_shown = ""
    current_line = 0
    stop_inds = [0, 0, 0, 0, 0, 0]
    fully_displayed = False

def initialize_font(n_screen, SCALE):
    global GAME_FONT
    global screen
    global scale
    global font_size
    
    font_size = 9 * SCALE
    screen = n_screen
    scale = SCALE
    GAME_FONT = pygame.font.Font('freesansbold.ttf', font_size)

def render_text():
    global GAME_FONT
    global screen
    global text_shown
    global stop_inds

    #GAME_FONT.render_to(screen, (15 * scale, (100) * scale), text_shown[0 : stop_inds[0]], (255, 255, 255))
    #GAME_FONT.render_to(screen, (15 * scale, (100) * scale + font_size), text_shown[stop_inds[0] : stop_inds[1]], (255, 255, 255))
    #GAME_FONT.render_to(screen, (15 * scale, (100) * scale + 2 * font_size), text_shown[stop_inds[1] : stop_inds[2]], (255, 255, 255))
    #GAME_FONT.render_to(screen, (15 * scale, (100) * scale + 3 * font_size), text_shown[stop_inds[2] : stop_inds[3]], (255, 255, 255))
    #GAME_FONT.render_to(screen, (15 * scale, (100) * scale + 4 * font_size), text_shown[stop_inds[3] : stop_inds[4]], (255, 255, 255))
    #GAME_FONT.render_to(screen, (15 * scale, (100) * scale + 5 * font_size), text_shown[stop_inds[4] : stop_inds[5]], (255, 255, 255))

    screen.blit(GAME_FONT.render(text_shown[0 : stop_inds[0]], True, 'white'), (15 * scale, (100) * scale))
    screen.blit(GAME_FONT.render(text_shown[stop_inds[0] : stop_inds[1]], True, 'white'), (15 * scale, (100) * scale + font_size))
    screen.blit(GAME_FONT.render(text_shown[stop_inds[1] : stop_inds[2]], True, 'white'), (15 * scale, (100) * scale + 2 * font_size))
    screen.blit(GAME_FONT.render(text_shown[stop_inds[2] : stop_inds[3]], True, 'white'), (15 * scale, (100) * scale + 3 * font_size))
    screen.blit(GAME_FONT.render(text_shown[stop_inds[3] : stop_inds[4]], True, 'white'), (15 * scale, (100) * scale + 4 * font_size))
    screen.blit(GAME_FONT.render(text_shown[stop_inds[4] : stop_inds[5]], True, 'white'), (15 * scale, (100) * scale + 5 * font_size))

def select_enter():
    global select
    select = True

