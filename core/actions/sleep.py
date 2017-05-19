from core.action import Action
from core.validators import *

class sleep(Action):
    name = "sleep"
    info = """Sleep is action that command device to wait fixed miliseconds before execute next action. 

Belowe payload will command device to wait 1s before executing next action:

sleep(1000)
    """
    short_description = """Sleep provided number of miliseconds."""

    def validate(self, payload):
           if len(payload) != 1:
              return "invalid use of sleep - it takes only one argument - see info argument sleep" 
           return "" if is_number(payload[0],True) else "Error - sleep takes positive integer as argument!"

    def __str__(self):
        return self.name

def init():
        return sleep()
