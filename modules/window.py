""" # old tkinter
import tkinter as tk
from tkinter import ttk

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, round(y * 0.7)))
    win.deiconify()

def start_window(x, y):
    root = tk.Tk()
    root.title("Homebase")
    
    root.geometry(str(x) + "x" + str(y))
    center(root)

    root.after(1, lambda: root.focus_force())

    # icon_img = tk.Image("photo", "../images/icon.png")
    # root.tk.call('wm','iconphoto', root._w, icon_img)
    
    # root.iconbitmap("../images/icon.icns")

    root.mainloop()

"""

# new pygame

import pygame, sys
from pygame.locals import *
from .controller import *
from .log import *
from .stdlib import *
from .audio import *
from .radio import *
import math
import time
import uuid

SURFACE = None
NAVBALL = None
MARKER = None
JOYSTICK_POS = None
ROCKET_POS = None
CONTROLLER_MARKER = None

THREAD_SHOULD_CLOSE = False

IGNORE_ROLL = False

AUDIO_ON = True

going_to_play = []
keys = {}

def get_key_down(key):
    try:
        return keys[ord(key)]
    except KeyError:
        return False

def get_key_up(key):
    try:
        return keys[ord(key)]
    except KeyError:
        return False

def should_play(*args):
    going_to_play.append((uuid.uuid4(), args))

def rot_center(image, angle, x, y):
    """
    loc = image.get_rect().center
    rot_sprite = pygame.transform.rotate(image, angle)
    rot_sprite.get_rect().center = loc
    return rot_sprite
    """

    # calcaulate the axis aligned bounding box of the rotated image
    w, h         = image.get_size()
    originPos = (w // 2, h // 2)
    pos = (x, y)
    sin_a, cos_a = math.sin(math.radians(angle)), math.cos(math.radians(angle))
    min_x, min_y = min([0, sin_a*h, cos_a*w, sin_a*h + cos_a*w]), max([0, sin_a*w, -cos_a*h, sin_a*w - cos_a*h])

    # calculate the translation of the pivot
    pivot        = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move   = pivot_rotate - pivot

    # calculate the upper left origin of the rotated image
    origin = (pos[0] - originPos[0] + min_x - pivot_move[0], pos[1] - originPos[1] - min_y + pivot_move[1])

    # get a rotated image
    rotated_image = pygame.transform.rotate(image, angle)

    # rotate and blit the image
    SURFACE.blit(rotated_image, origin)

def render_image(image, x, y):
    if not SURFACE or not image:
        assert False

    SURFACE.blit(image, (x, y))

def start_window(x, y):
    global SURFACE
    log("starting main window")
    pygame.init()
    SURFACE = pygame.display.set_mode((x, y))
    pygame.display.set_caption("Homebase")
    pygame.joystick.init()

def place_navball(x, y, z):
    global NAVBALL
    if not SURFACE or not NAVBALL:
        assert False

    rot_center(NAVBALL, z, x, y)
    # SURFACE.blit(NAVBALL, (x, y))

def place_marker(x, y):
    if not SURFACE or not MARKER:
        assert False

    SURFACE.blit(MARKER, (x, y))

def place_controller_marker(x, y, z):
    global CONTROLLER_MARKER
    if not SURFACE or not NAVBALL:
        assert False

    rot_center(CONTROLLER_MARKER, z, x, y)

def kill_local_threads():
    global THREAD_SHOULD_CLOSE
    log("killing all local threads")
    THREAD_SHOULD_CLOSE = True

def window_loop(width, height):
    global NAVBALL, MARKER, IGNORE_ROLL, JOYSTICK_POS, ROCKET_POS, CONTROLLER_MARKER
    log("starting main window loop")
    if not SURFACE:
        assert False

    NAVBALL = pygame.image.load("images/navball.png")
    MARKER = pygame.image.load("images/marker.png")
    CONTROLLER_MARKER = pygame.image.load("images/controller_marker.png")

    controller = Controller()
    controller.init()
    x = (width / 2) #- (NAVBALL.get_width() / 2)
    y = (height / 2) #- (NAVBALL.get_height() / 2)
    z = 0

    orient_x, orient_y, orient_z = 0, 0, 0

    m_x = (width / 2) - (MARKER.get_width() / 2)
    m_y = (height / 2) - (MARKER.get_height() / 2)

    radio_open("") # XXX: add real serial

    add_thread(__thread___joystick_button, (), "_joystick_button")
    add_thread(__thread___audio_dameon, (), "_audio_dameon")
    add_thread(__thread___keybind_dameon, (), "_keybind_dameon")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                # print()
                log("we gun die")
                radio_close()
                kill_local_threads()
                exit()
                # send_exit()

            if event.type == pygame.JOYAXISMOTION:
                controller.axis_data[event.axis] = round(event.value, 2)
            elif event.type == pygame.JOYBUTTONDOWN:
                controller.button_data[event.button] = True
            elif event.type == pygame.JOYBUTTONUP:
                controller.button_data[event.button] = False
            elif event.type == pygame.JOYHATMOTION:
                controller.hat_data[event.hat] = event.value

            if event.type == pygame.KEYDOWN:
                keys[event.key] = True
            elif event.type == pygame.KEYUP:
                keys[event.key] = False

        try:
            controller_x = controller.listen()[1][0]
            controller_y = controller.listen()[1][1]
            controller_z = controller.listen()[1][2]
            JOYSTICK_POS = controller.listen()
        except KeyError:
            controller_x, controller_y, controller_z = 0, 0, 0

        # TODO: Add some rocket IMU reading bullcrap here.
        try:
            orient_x, orient_y, orient_z = x, y, z
            ROCKET_POS = (orient_x, orient_y, orient_z)
        except BaseException: # XXX: Input some kind of error here.
            # XXX: Error handling here.
            pass

        SURFACE.fill((0, 0, 0))
        if not IGNORE_ROLL:
            # place_navball(x + (-controller_x * 90), y + (controller_y * 90), -controller_z * 10)
            place_navball(orient_x, orient_y, orient_z)
            place_controller_marker(x + (controller_x * 90), y + (controller_y * 90), -controller_z * 10)
            radio_send(radio_types.CONTROLLER_INPUT, controller_x, controller_y, controller_z)
        else:
            # place_navball(x + (-controller_x * 90), y + (controller_y * 90), 0)
            place_navball(orient_x, orient_y, orient_z)
            place_controller_marker(x + (controller_x * 90), y + (controller_y * 90), 0)
            radio_send(radio_types.CONTROLLER_INPUT, controller_x, controller_y, 0)
        # place_navball(x, y, 10)
        place_marker(m_x, m_y)
        
        # print(controller.listen(), end = "\r")
        pygame.display.update()

def __thread___joystick_button():
    global JOYSTICK_POS, IGNORE_ROLL
    log("thread _joystick_button begin")
    while True:
        if THREAD_SHOULD_CLOSE:
            log("thread _joystick_button stop")
            break

        if JOYSTICK_POS == None:
            continue
        button_state = JOYSTICK_POS[0][1]

        if not button_state:
            continue
        else:
            while JOYSTICK_POS[0][1]: pass
            IGNORE_ROLL = not IGNORE_ROLL
            if IGNORE_ROLL:
                log("locked roll")
                should_play("controller", "roll", "locked")
            else:
                log("unlocked roll")
                should_play("controller", "roll", "unlocked")

def __thread___audio_dameon():
    log("thread _audio_dameon begin")
    open_audio("tcas_audio_2")
    play("audio", "on")
    said_audio_off = False
    while True:
        if THREAD_SHOULD_CLOSE:
            log("thread _audio_dameon stop")
            break

        if not AUDIO_ON and not said_audio_off:
            said_audio_off = True
            play("audio", "off")
        elif AUDIO_ON and said_audio_off:
            said_audio_off = False
            play("audio", "on")
    
        if len(going_to_play) <= 0:
            continue
        else:
            for i in going_to_play:
                args = i[1]
                for ii in args:
                    if AUDIO_ON:
                        play_one(ii)
                going_to_play.remove(i)
                time.sleep(0.2)

    close_audio()

def __thread___keybind_dameon():
    global AUDIO_ON
    log("thread _keybind_dameon begin")

    while True:
        if THREAD_SHOULD_CLOSE:
            log("thread _keybind_dameon stop")
            break
        
        if get_key_down('a'):
            while get_key_down('a'): pass
            AUDIO_ON = not AUDIO_ON
            if AUDIO_ON:
                log("audio on")
            else:
                log("audio off")
