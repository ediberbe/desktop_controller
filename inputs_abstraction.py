"""Abstracts the Inputs module for the XBOX controller. Is this high level enough?"""

# pylint: disable = protected-access, line-too-long

import inputs

# "Y","X","B","A",None,None,"RB","LB","RSB","LSB","BACK","MENU","R","L","D","U"
# "LT","RT","LSX","LSY","RSX","RSY"

def get_controllers():
    """
    Returns: List of connected xbox controllers.
    """
    return inputs.devices.gamepads

def get_state(index):
    """
    Args: Position of controller in list
    Returns: State object of target controller
    """
    state = inputs.devices.gamepads[index]._GamePad__read_device()
    state.index = index
    return state

def get_buttons(state):
    """
    Args: State object of target controller
    Returns: List of button states
    """
    buttons_state = inputs.devices.gamepads[state.index]._GamePad__get_bit_values(state.gamepad.buttons, 16)
    buttons = []
    for i in buttons_state:
        buttons.append(i)

    return buttons

def get_axes(state):
    """
    Args: State object of target controller
    Returns: List of axis states
    """
    axes_fields = dict(inputs.XinputGamepad._fields_)
    axes_fields.pop('buttons')

    axes = []
    for axis, _ in list(axes_fields.items()):
        value = getattr(state.gamepad, axis)
        axes.append(value)

    return axes

def get_event(index):
    """NOT TO BE USED"""
    gamepad = inputs.devices.gamepads[index]
    events = gamepad.read()
    for event in events:
        if event.ev_type != "Sync":
            print(event.ev_type, event.code, event.state)

# EXAMPLE CODE

# import inputs_abstraction as ia

# while True:
#     state = ia.get_state(0)

#     buttons = ia.get_buttons(state)
#     print(ia.labelsort_list(buttons, ia.XBOX_BUTTONS_SORT, ia.XBOX_BUTTONS_LABEL))

#     axes = ia.get_axes(state)
#     print(ia.labelsort_list(axes, ia.XBOX_AXES_SORT, ia.XBOX_AXES_LABEL))
