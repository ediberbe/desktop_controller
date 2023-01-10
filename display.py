"""docstring"""

# pylint: disable = no-member, too-many-function-args, global-statement, invalid-name, line-too-long, unexpected-keyword-arg

import ctypes
from ctypes import wintypes
import pygame as pg

pg.init()

WIDTH = 320
HEIGHT = 320
SCALE = 1

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MONITOR = pg.display.Info()
SCREEN = pg.Surface([WIDTH, HEIGHT])
WINDOW = None

IS_ON = False

def stop():
    """Closes window."""
    global IS_ON
    pg.display.quit()
    IS_ON = False

def start():
    """Opens window."""
    global WINDOW, WIDTH, HEIGHT, SCALE, MONITOR, IS_ON
    pg.init()
    pg.display.set_caption("desktop_controller")
    ICON = pg.image.load("img/cog.png")
    pg.display.set_icon(ICON)
    #SetWindowPos = ctypes.windll.user32.SetWindowPos
    WINDOW = pg.display.set_mode((int(WIDTH * SCALE), int(HEIGHT * SCALE)),pg.NOFRAME)
    
    hwnd = pg.display.get_wm_info()['window']
    user32 = ctypes.WinDLL("user32")
    user32.SetWindowPos.restype = wintypes.HWND
    user32.SetWindowPos.argtypes = [wintypes.HWND, wintypes.HWND, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.INT, wintypes.UINT]
    user32.SetWindowPos(pg.display.get_wm_info()['window'], -1,  MONITOR.current_w - WIDTH - 100, MONITOR.current_h - HEIGHT - 100, 0, 0, 0x0001)

    IS_ON = True

def change_color(img, color):
    """docstring"""
    # Remove Color
    aux = pg.Surface((img.get_width(), img.get_height()), flags=pg.SRCALPHA)
    aux.fill((255, 255, 255, 0))
    img.blit(aux, (0, 0), special_flags=pg.BLEND_RGBA_SUB)
    # Add desired color
    aux.fill(color + (0,))
    img.blit(aux, (0, 0), special_flags=pg.BLEND_RGBA_ADD)

def run(toggle_keyboard, keeb_select1, keeb_select2, modifier, background_color, foreground_color, select_color):
    """To be put in controller run function"""
    global SCREEN, WIDTH, SCALE, HEIGHT, WINDOW, IS_ON
    if IS_ON:
        # DRAW
        SCREEN.fill(background_color)
        foreground = pg.image.load("img/"+str(keeb_select1)+str(modifier)+".png")
        change_color(foreground, foreground_color)
        SCREEN.blit(foreground, (0, 0))
        select = pg.image.load("img/square.png")
        change_color(select, select_color)
        SCREEN.blit(select, (keeb_select2%3*106, keeb_select2//3*106))

        # UPDATE
        pg.transform.scale(SCREEN, (int(WIDTH * SCALE), int(HEIGHT * SCALE)), WINDOW)
        pg.display.update()

        # EVENT
        for event in pg.event.get():
            if event.type == pg.QUIT:
                toggle_keyboard()
