"""Control mouse/keyboard using xbox controller."""

# pylint: disable = unused-import, bad-continuation, c-extension-no-member, line-too-long, unused-variable, unnecessary-lambda, bad-whitespace, invalid-name, attribute-defined-outside-init

from math import trunc
import configparser
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import Vector2, time # length, scale_to_length, normalize, angle_to(Vector2())
import pynput
import inputs_abstraction as ia
import display as dp
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()

class Xboxcontroller:
    """Singleton class, instance is XBOXCONTROLLER"""
    def __init__(self):
        self.read_config("config.ini")

        self.index = None
        self.state = None

        self.bts = []
        self.axs = []
        self.old_bts = []
        self.old_axs = []

        self.modifier = False
        def set_modifier(value):
            self.modifier = value

        self.keeb_mode = False
        self.keeb_select1 = 0 # Big Box
        self.keeb_select2 = 4 # Small Box
        def set_keeb_select1(value):
            self.keeb_select1 = value
        def set_keeb_select2(value):
            self.keeb_select2 = value
        self.keeb_values1 = [["1","2","3","4","5","6","7","8","9"],
                            ["r","t","y","f","g","h","v","b","n"],
                            ["u","i","o","j","k","p","m","0","l"],
                            ["-","[","]","=",";","'",",",".","/"],
                            ["q","w","e","a","s","d","z","x","c"]]
        self.keeb_values2 = [["!","@","#","$","%","^","&","*","("],
                             ["R","T","Y","F","G","H","V","B","N"],
                             ["U","I","O","J","K","P","M",")","L"],
                             ["_","{","}","+",":","\"","<",">","?"],
                             ["Q","W","E","A","S","D","Z","X","C"]]
        def keyboard_tap(key, modifier=None, count=1):
            for i in range(count):
                if modifier is None:
                    keyboard.press(key)
                    keyboard.release(key)
                else:
                    keyboard.press(modifier)
                    keyboard.press(key)
                    keyboard.release(key)
                    keyboard.release(modifier)

        self.selected_button_binds = 1
        self.button_binds = [{  # PRINT
            0: [lambda: None, lambda: print("Y PRESS"), lambda: None, lambda: print("MODIFIED Y PRESS")], # Y
            1: [lambda: None, lambda: print("X PRESS"), lambda: None, lambda: print("MODIFIED X PRESS")], # X
            2: [lambda: None, lambda: print("B PRESS"), lambda: None, lambda: print("MODIFIED B PRESS")], # B
            3: [lambda: None, lambda: print("A PRESS"), lambda: None, lambda: print("MODIFIED A PRESS")], # A
            4: [lambda: None, lambda: None, lambda: None, lambda: None],
            5: [lambda: None, lambda: None, lambda: None, lambda: None],
            6: [lambda: None, lambda: print("RB PRESS"), lambda: None, lambda: print("MODIFIED RB PRESS")], # RB
            7: [lambda: None, lambda: print("LB PRESS"), lambda: None, lambda: print("MODIFIED LB PRESS")], # LB
            8: [lambda: None, lambda: print("RSB PRESS"), lambda: None, lambda: print("MODIFIED RSB PRESS")], # RSB
            9: [lambda: None, lambda: print("LSB PRESS"), lambda: None, lambda: print("MODIFIED LSB PRESS")], # LSB
            10: [lambda: None, lambda: print("BACK PRESS"), lambda: None, lambda: print("MODIFIED BACK PRESS")], # BACK
            11: [lambda: None, lambda: print("MENU PRESS"), lambda: None, lambda: print("MODIFIED MENU PRESS")], # MENU
            12: [lambda: None, lambda: print("R PRESS"), lambda: None, lambda: print("MODIFIED R PRESS")], # R
            13: [lambda: None, lambda: print("L PRESS"), lambda: None, lambda: print("MODIFIED L PRESS")], # L
            14: [lambda: None, lambda: print("D PRESS"), lambda: None, lambda: print("MODIFIED D PRESS")], # D
            15: [lambda: None, lambda: print("U PRESS"), lambda: None, lambda: print("MODIFIED U PRESS")] # U
        },
        {   # MOUSE
            0: [lambda: None, lambda: keyboard_tap("m", pynput.keyboard.Key.cmd), lambda: None, lambda: keyboard_tap("=", pynput.keyboard.Key.ctrl)], # Y
            1: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.media_volume_mute), lambda: None, lambda: keyboard_tap("-", pynput.keyboard.Key.ctrl)], # X
            2: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.media_volume_up, count=2), lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.right, pynput.keyboard.Key.alt)], # B
            3: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.media_volume_down, count=2), lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.left, pynput.keyboard.Key.alt)], # A
            4: [lambda: None, lambda: None, lambda: None, lambda: None],
            5: [lambda: None, lambda: None, lambda: None, lambda: None],
            6: [lambda: mouse.release(pynput.mouse.Button.right), lambda: mouse.press(pynput.mouse.Button.right), lambda: mouse.release(pynput.mouse.Button.right), lambda: mouse.press(pynput.mouse.Button.right)], # RB
            7: [lambda: mouse.release(pynput.mouse.Button.left), lambda: mouse.press(pynput.mouse.Button.left), lambda: mouse.release(pynput.mouse.Button.left), lambda: mouse.press(pynput.mouse.Button.left)], # LB
            8: [lambda: None, lambda: None, lambda: None, lambda: None], # RSB
            9: [lambda: None, lambda: None, lambda: None, lambda: None], # LSB
            10: [lambda: None, lambda: self.toggle_keyboard(), lambda: None, lambda: None], # BACK
            11: [lambda: None, lambda: toggle_lock(), lambda: None, lambda: toggle_lock()], # MENU
            12: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.right), lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.end)], # R
            13: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.left), lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.home)], # L
            14: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.down), lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.page_down)], # D
            15: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.up), lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.page_up)] # U
        },
        {   # KEYBOARD
            0: [lambda: None, lambda: None, lambda: None, lambda: None], # Y
            1: [lambda: None, lambda: None, lambda: None, lambda: None], # X
            2: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.enter), lambda: None, lambda: None], # B
            3: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.space), lambda: None, lambda: None], # A
            4: [lambda: None, lambda: None, lambda: None, lambda: None],
            5: [lambda: None, lambda: None, lambda: None, lambda: None],
            6: [lambda: None, lambda: keyboard.type(self.keeb_values1[self.keeb_select1][self.keeb_select2]), lambda: None, lambda: keyboard.type(self.keeb_values2[self.keeb_select1][self.keeb_select2])], # RB
            7: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.backspace), lambda: None, lambda: keyboard_tap("a", pynput.keyboard.Key.ctrl)], # LB
            8: [lambda: None, lambda: None, lambda: None, lambda: None], # RSB
            9: [lambda: None, lambda: None, lambda: None, lambda: None], # LSB
            10: [lambda: None, lambda: self.toggle_keyboard(), lambda: None, lambda: None], # BACK
            11: [lambda: None, lambda: toggle_lock(), lambda: None, lambda: toggle_lock()], # MENU
            12: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.right), lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.end)], # R
            13: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.left), lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.home)], # L
            14: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.down), lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.page_down)], # D
            15: [lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.up), lambda: None, lambda: keyboard_tap(pynput.keyboard.Key.page_up)] # U
        },
        {   # LOCK
            0: [lambda: None, lambda: None, lambda: None, lambda: None], # Y
            1: [lambda: None, lambda: None, lambda: None, lambda: None], # X
            2: [lambda: None, lambda: None, lambda: None, lambda: None], # B
            3: [lambda: None, lambda: None, lambda: None, lambda: None], # A
            4: [lambda: None, lambda: None, lambda: None, lambda: None],
            5: [lambda: None, lambda: None, lambda: None, lambda: None],
            6: [lambda: None, lambda: None, lambda: None, lambda: None], # RB
            7: [lambda: None, lambda: None, lambda: None, lambda: None], # LB
            8: [lambda: None, lambda: None, lambda: None, lambda: None], # RSB
            9: [lambda: None, lambda: None, lambda: None, lambda: None], # LSB
            10: [lambda: None, lambda: None, lambda: None, lambda: None], # BACK
            11: [lambda: None, lambda: toggle_lock(), lambda: None, lambda: toggle_lock()], # MENU
            12: [lambda: None, lambda: None, lambda: None, lambda: None], # R
            13: [lambda: None, lambda: None, lambda: None, lambda: None], # L
            14: [lambda: None, lambda: None, lambda: None, lambda: None], # D
            15: [lambda: None, lambda: None, lambda: None, lambda: None] # U
        }]

        self.selected_axis_binds = 1
        self.axis_binds = [{    # PRINT
            "LTN": [lambda: None, lambda: print("LTN PRESS"), lambda: None, lambda: print("MODIFIED LTN PRESS")],
            "LTS": [lambda: None, lambda: print("LTS PRESS"), lambda: None, lambda: print("MODIFIED LTS PRESS")],
            "LTF": [lambda: None, lambda: print("LTF PRESS"), lambda: None, lambda: print("MODIFIED LTF PRESS")],

            "RTN": [lambda: None, lambda: print("RTN PRESS"), lambda: None, lambda: print("MODIFIED RTN PRESS")],
            "RTS": [lambda: None, lambda: print("RTS PRESS"), lambda: None, lambda: print("MODIFIED RTS PRESS")],
            "RTF": [lambda: None, lambda: print("RTF PRESS"), lambda: None, lambda: print("MODIFIED RTF PRESS")],

            "LSN": [lambda: None, lambda: print("LSN PRESS"), lambda: None, lambda: print("MODIFIED LSN PRESS")],
            "LSU": [lambda: None, lambda: print("LSU PRESS"), lambda: None, lambda: print("MODIFIED LSU PRESS")],
            "LSUR": [lambda: None, lambda: print("LSUR PRESS"), lambda: None, lambda: print("MODIFIED LSUR PRESS")],
            "LSR": [lambda: None, lambda: print("LSR PRESS"), lambda: None, lambda: print("MODIFIED LSR PRESS")],
            "LSDR": [lambda: None, lambda: print("LSDR PRESS"), lambda: None, lambda: print("MODIFIED LSDR PRESS")],
            "LSD": [lambda: None, lambda: print("LSD PRESS"), lambda: None, lambda: print("MODIFIED LSD PRESS")],
            "LSDL": [lambda: None, lambda: print("LSDL PRESS"), lambda: None, lambda: print("MODIFIED LSDL PRESS")],
            "LSL": [lambda: None, lambda: print("LSL PRESS"), lambda: None, lambda: print("MODIFIED LSL PRESS")],
            "LSUL": [lambda: None, lambda: print("LSUL PRESS"), lambda: None, lambda: print("MODIFIED LSUL PRESS")],

            "RSN": [lambda: None, lambda: print("RSN PRESS"), lambda: None, lambda: print("MODIFIED RSN PRESS")],
            "RSU": [lambda: None, lambda: print("RSU PRESS"), lambda: None, lambda: print("MODIFIED RSU PRESS")],
            "RSUR": [lambda: None, lambda: print("RSUR PRESS"), lambda: None, lambda: print("MODIFIED RSUR PRESS")],
            "RSR": [lambda: None, lambda: print("RSR PRESS"), lambda: None, lambda: print("MODIFIED RSR PRESS")],
            "RSDR": [lambda: None, lambda: print("RSDR PRESS"), lambda: None, lambda: print("MODIFIED RSDR PRESS")],
            "RSD": [lambda: None, lambda: print("RSD PRESS"), lambda: None, lambda: print("MODIFIED RSD PRESS")],
            "RSDL": [lambda: None, lambda: print("RSDL PRESS"), lambda: None, lambda: print("MODIFIED RSDL PRESS")],
            "RSL": [lambda: None, lambda: print("RSL PRESS"), lambda: None, lambda: print("MODIFIED RSL PRESS")],
            "RSUL": [lambda: None, lambda: print("RSUL PRESS"), lambda: None, lambda: print("MODIFIED RSUL PRESS")]
        },
        {   # MOUSE
            "LTN": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LTS": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LTF": [lambda: None, lambda: set_modifier(True), lambda: set_modifier(False), lambda: None],

            "RTN": [lambda: mouse.scroll(0, -1), lambda: None, lambda: mouse.scroll(0, 1), lambda: None],
            "RTS": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RTF": [lambda: None, lambda: mouse.scroll(0, -2), lambda: None, lambda: mouse.scroll(0, 2)],

            "LSN": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSU": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSUR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSDR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSD": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSDL": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSL": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSUL": [lambda: None, lambda: None, lambda: None, lambda: None],

            "RSN": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSU": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSUR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSDR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSD": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSDL": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSL": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSUL": [lambda: None, lambda: None, lambda: None, lambda: None],
        },
        {   # KEYBOARD
            "LTN": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LTS": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LTF": [lambda: None, lambda: set_modifier(True), lambda: set_modifier(False), lambda: None],

            "RTN": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RTS": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RTF": [lambda: None, lambda: None, lambda: None, lambda: None],

            "LSN": [lambda: None, lambda: set_keeb_select1(0), lambda: None, lambda: set_keeb_select1(0)],
            "LSU": [lambda: None, lambda: set_keeb_select1(1), lambda: None, lambda: set_keeb_select1(1)],
            "LSUR": [lambda: None, lambda: set_keeb_select1(1), lambda: None, lambda: set_keeb_select1(1)],
            "LSR": [lambda: None, lambda: set_keeb_select1(2), lambda: None, lambda: set_keeb_select1(2)],
            "LSDR": [lambda: None, lambda: set_keeb_select1(2), lambda: None, lambda: set_keeb_select1(2)],
            "LSD": [lambda: None, lambda: set_keeb_select1(3), lambda: None, lambda: set_keeb_select1(3)],
            "LSDL": [lambda: None, lambda: set_keeb_select1(3), lambda: None, lambda: set_keeb_select1(3)],
            "LSL": [lambda: None, lambda: set_keeb_select1(4), lambda: None, lambda: set_keeb_select1(4)],
            "LSUL": [lambda: None, lambda: set_keeb_select1(4), lambda: None, lambda: set_keeb_select1(4)],

            "RSN": [lambda: None, lambda: set_keeb_select2(4), lambda: None, lambda: set_keeb_select2(4)],
            "RSU": [lambda: None, lambda: set_keeb_select2(1), lambda: None, lambda: set_keeb_select2(1)],
            "RSUR": [lambda: None, lambda: set_keeb_select2(2), lambda: None, lambda: set_keeb_select2(2)],
            "RSR": [lambda: None, lambda: set_keeb_select2(5), lambda: None, lambda: set_keeb_select2(5)],
            "RSDR": [lambda: None, lambda: set_keeb_select2(8), lambda: None, lambda: set_keeb_select2(8)],
            "RSD": [lambda: None, lambda: set_keeb_select2(7), lambda: None, lambda: set_keeb_select2(7)],
            "RSDL": [lambda: None, lambda: set_keeb_select2(6), lambda: None, lambda: set_keeb_select2(6)],
            "RSL": [lambda: None, lambda: set_keeb_select2(3), lambda: None, lambda: set_keeb_select2(3)],
            "RSUL": [lambda: None, lambda: set_keeb_select2(0), lambda: None, lambda: set_keeb_select2(0)],
        },
        {   # LOCK
            "LTN": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LTS": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LTF": [lambda: None, lambda: set_modifier(True), lambda: set_modifier(False), lambda: None],

            "RTN": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RTS": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RTF": [lambda: None, lambda: None, lambda: None, lambda: None],

            "LSN": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSU": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSUR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSDR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSD": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSDL": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSL": [lambda: None, lambda: None, lambda: None, lambda: None],
            "LSUL": [lambda: None, lambda: None, lambda: None, lambda: None],

            "RSN": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSU": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSUR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSDR": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSD": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSDL": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSL": [lambda: None, lambda: None, lambda: None, lambda: None],
            "RSUL": [lambda: None, lambda: None, lambda: None, lambda: None],
        }]

        self.mouse_xsp = 0 # subpixel value
        self.mouse_ysp = 0 # subpixel value

        self.clock = time.Clock()

        self.is_lock = False
        def toggle_lock():
            if not self.is_lock:
                self.is_lock = True
                print("Controller locked.")
                self.old_sbb = self.selected_button_binds
                self.selected_button_binds = 3

                self.old_sab = self.selected_axis_binds
                self.selected_axis_binds = 3
            else:
                self.is_lock = False
                print("Controller unlocked.")
                self.selected_button_binds = self.old_sbb
                self.selected_axis_binds = self.old_sab


        self.select_controller()

    def read_config(self, filename):
        """Called at object init. Changes variables according to config file."""
        read_config = configparser.ConfigParser()
        read_config.read(filename)

        self.trigger_max = int(read_config.get("Thresholds", "trigger_max"))
        self.stick_deadzone = int(read_config.get("Thresholds", "stick_deadzone"))
        self.mouse_deadzone = int(read_config.get("Thresholds", "mouse_deadzone"))

        self.curve_sensitivity = int(read_config.get("Mouse", "curve_sensitivity"))
        self.mouse_lspeed1 = int(read_config.get("Mouse", "mouse_lspeed1"))
        self.mouse_lspeed2 = int(read_config.get("Mouse", "mouse_lspeed2"))
        self.mouse_rspeed1 = int(read_config.get("Mouse", "mouse_rspeed1"))
        self.mouse_rspeed2 = int(read_config.get("Mouse", "mouse_rspeed2"))

        self.polling_rate = int(read_config.get("Other", "polling_rate"))

        self.background_color = read_config.get("Color", "background_color")
        self.background_color = (int((self.background_color.split(","))[0]),int((self.background_color.split(","))[1]),int((self.background_color.split(","))[2]))
        self.foreground_color = read_config.get("Color", "foreground_color")
        self.foreground_color = (int((self.foreground_color.split(","))[0]),int((self.foreground_color.split(","))[1]),int((self.foreground_color.split(","))[2]))
        self.select_color = read_config.get("Color", "select_color")
        self.select_color = (int((self.select_color.split(","))[0]),int((self.select_color.split(","))[1]),int((self.select_color.split(","))[2]))

    def select_controller(self):
        """Called at object init. Selects controller from list of connected controllers."""
        controller_list = ia.get_controllers()

        if len(controller_list) == 0:
            print("No controller found. Closing in 5 seconds.")
            self.clock.tick(1/5)
            exit()

        elif len(controller_list) == 1:
            print("1 controller found.")
            self.index = 0

        else:
            print(len(controller_list), "controllers found.")
            self.index = int(input("Select controller: "))-1

    def button_press(self):
        """Detects button changes and acts according to self.button_binds."""
        self.bts = ia.get_buttons(self.state)

        # CHANGE
        if self.old_bts:
            for i, _ in enumerate(self.bts):
                if self.bts[i] != self.old_bts[i]:
                    if not self.modifier:
                        self.button_binds[self.selected_button_binds][i][self.bts[i]]()
                    else:
                        self.button_binds[self.selected_button_binds][i][self.bts[i]+2]()

        # ROTATE
        self.old_bts = self.bts
        self.bts = []

    def axis_press(self):
        """Detects axis changes and acts according to self.axis_binds."""
        aux = ia.get_axes(self.state)
        leftstick = Vector2(aux[2], aux[3])
        ls_angle = -leftstick.angle_to(Vector2())
        rightstick = Vector2(aux[4], aux[5])
        rs_angle = -rightstick.angle_to(Vector2())

        # TRIGGER TRANSFORM
        if aux[0] == 0:
            self.axs.append("LTN")
        elif aux[0] == self.trigger_max:
            self.axs.append("LTF")
        else:
            self.axs.append("LTS")

        if aux[1] == 0:
            self.axs.append("RTN")
        elif aux[1] == self.trigger_max:
            self.axs.append("RTF")
        else:
            self.axs.append("RTS")

        # STICK TRANSFORM
        lstransform = {
            -1: "LSL",
            0: "LSDL",
            1: "LSD",
            2: "LSDR",
            3: "LSR",
            4: "LSUR",
            5: "LSU",
            6: "LSUL",
            7: "LSL"
        }
        rstransform = {
            -1: "RSL",
            0: "RSDL",
            1: "RSD",
            2: "RSDR",
            3: "RSR",
            4: "RSUR",
            5: "RSU",
            6: "RSUL",
            7: "RSL"
        }

        if leftstick.length() < self.stick_deadzone:
            self.axs.append("LSN")
        else:
            self.axs.append(lstransform[int((ls_angle+157.5)//45)])

        if rightstick.length() < self.stick_deadzone:
            self.axs.append("RSN")
        else:
            self.axs.append(rstransform[int((rs_angle+157.5)//45)])

        # CHANGE
        if self.old_axs:
            for i, _ in enumerate(self.axs):
                if self.axs[i] != self.old_axs[i]:
                    if not self.modifier:
                        self.axis_binds[self.selected_axis_binds][self.old_axs[i]][0]()
                        self.axis_binds[self.selected_axis_binds][self.axs[i]][1]()
                    else:
                        self.axis_binds[self.selected_axis_binds][self.old_axs[i]][2]()
                        self.axis_binds[self.selected_axis_binds][self.axs[i]][3]()

        # ROTATE
        self.old_axs = self.axs
        self.axs = []

    def axis_mouse(self, is_ls=True):
        """Moves mouse according to rightstick."""
        aux = ia.get_axes(self.state)

        if is_ls:
            stick = Vector2(aux[2], aux[3])
            if self.modifier:
                mouse_speed = self.mouse_lspeed2
            else:
                mouse_speed = self.mouse_lspeed1

        else:
            stick = Vector2(aux[4], aux[5])
            if self.modifier:
                mouse_speed = self.mouse_rspeed2
            else:
                mouse_speed = self.mouse_rspeed1

        def windows_rc(i, s):
            """https://github.com/achilleas-k/fs2open.github.com/blob/joystick_curves/joy_curve_notes/new_curves.md"""
            return i**(3-(s/4.5))

        if stick.length() > self.mouse_deadzone:
            stick.scale_to_length(windows_rc(stick.length()/39367, self.curve_sensitivity))
            self.mouse_xsp = self.mouse_xsp + (stick.x * mouse_speed)
            self.mouse_ysp = self.mouse_ysp + (stick.y * mouse_speed)
            mouse.move(trunc(self.mouse_xsp), -trunc(self.mouse_ysp))
            self.mouse_xsp = self.mouse_xsp - trunc(self.mouse_xsp)
            self.mouse_ysp = self.mouse_ysp - trunc(self.mouse_ysp)

    def toggle_keyboard(self):
        """docstring"""
        if self.keeb_mode:
            self.keeb_mode = False
            self.selected_button_binds = 1
            self.selected_axis_binds = 1
            dp.stop()
        else:
            self.keeb_mode = True
            self.selected_button_binds = 2
            self.selected_axis_binds = 2
            dp.start()
            mouse.press(pynput.mouse.Button.left)
            mouse.release(pynput.mouse.Button.left)

    def run(self):
        """To be put inside main loop."""
        try:
            self.state = ia.get_state(self.index)

            self.button_press()
            self.axis_press()

            if self.keeb_mode:
                dp.run(self.toggle_keyboard, self.keeb_select1, self.keeb_select2, self.modifier, self.background_color, self.foreground_color, self.select_color)

            elif not self.is_lock:
                self.axis_mouse(True)
                self.axis_mouse(False)

            self.clock.tick(self.polling_rate)

        except AttributeError:
            print("An error has occured. Please reconnect controller. Retrying in 5 seconds.")
            self.clock.tick(1/5)

XBOXCONTROLLER = Xboxcontroller()
