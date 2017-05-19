from core.action import Action
from core.validators import *

class mouse_click(Action):
    name = "mouse_click"
    info = """mouse_click is action for controling mouse buttons. It takes one argument with values:
- 0 : buttons released
- 1 : left button pressed
- 2 : right button pressed
- 3 : third button pressed (scroll button)

Belowe payload will command device to spoof mouse double-click:

mouse_click(1);
sleep(200);
mouse_click(0);
sleep(500);
mouse_click(1);
sleep(200);
mouse_click(0);

    """
    short_description = """Command device to spoof mouse click button 1,2 or 3."""

    def validate(self, payload):
        if len(payload)!=1:
            return "Invalid arguments - mouse_click takes 1 arguments. See info actions mouse_move"
        if not is_number(payload[0],True) or int(payload[0]) not in [0,1,2,3]:
                return "Error - mouse_click takes integer (0, 1, 2 or 3) as first argument! See info actions mouse_move."
        return ""


    def __str__(self):
        return self.name

def init():
        return mouse_click()

