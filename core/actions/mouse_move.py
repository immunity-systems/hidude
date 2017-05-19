from core.action import Action
from core.validators import *

class mouse_move(Action):
    name = "mouse_move"
    info = """mouse_move is action that command device to move cursor in x and y direction (values can be
from range -127 - 127 ).

Belowe payload will command device to move mouse 10 in x and y, wait 1s and go back:

mouse_move(10,10);
sleep(1000);
mouse_move(-10,-10);
    """
    short_description = """Move mouse in in x,y direction. Arguments can be negative."""

    def validate(self, payload):
        if len(payload)!=2:
            return "Invalid arguments - mouse_move takes 2 arguments. See info actions mouse_move"
        if not is_number(payload[0],False):
                return "Error - mouse_move takes integer (i.e. 127 or -127) as first argument! See info actions mouse_move."
        elif not is_number(payload[1],False):
                return "Error - mouse_move takes integer (i.e. 127 or -127) as second argument! See info actions mouse_move."
        return ""


    def __str__(self):
        return self.name

def init():
        return mouse_move()

