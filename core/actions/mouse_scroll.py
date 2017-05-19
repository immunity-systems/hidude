from core.action import Action
from core.validators import *

class mouse_scroll(Action):
    name = "mouse_scroll"
    info = """mouse_scroll is action that command device to spoof mouse scroll wheel (values can be
from range -127 - 127 and are relative to current scroll position in system).

Belowe payload will command device to scroll down 10 and wait 1s and go back:

mouse_scroll(10);
    """
    short_description = """Scroll wheel of mouse in up or down direction. Arguments can be negative."""

    def validate(self, payload):
        if len(payload)!=1:
            return "Invalid arguments - mouse_move takes 1 arguments. See info actions mouse_move"
        if not is_number(payload[0],False):
                return "Error - mouse_scroll takes integer (i.e. 127 or -127) as first argument! See info actions mouse_scroll."
        return ""


    def __str__(self):
        return self.name

def init():
        return mouse_scroll()

