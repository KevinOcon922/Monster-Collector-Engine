from pygame import time

dt = 0
fps = 60
clock = time.Clock()

def tick():
    global dt
    dt = clock.tick(fps)

def delta_time():
    global dt
    return dt

def update_fps(new_fps):
    global fps
    fps = new_fps