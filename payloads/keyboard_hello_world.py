__author__ = "Karol Celinski"
__copyright__ = "Copyright 2017, Immunity Systems Sp. z o.o."
__credits__ = ["Andrzej Nowodworski", "Pawel Maziarz"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Karol Celinski"
__email__ = "karolc@immunity-systems.com"

from core.payload import Payload
from core.validators import *

class keyboard_hello_world(Payload):
    """
    Name of payload.
    """
    name = "keyboard_hello_world"
    """
    Description.
    """
    info = """PoC for testing new device with keyboard abilities
It's simple sending constant string 'Hello World' and does nothing else ;-).
    """
    """
    Shor description
    """
    short_description = "Device after plugin writes 'Hello World' as a keyboard."
    """
    Abilities that is required by payload.
    """
    satisfied_actions = ['keyboard_write', 'sleep']
    
    parameters = {
                'uppercase': {
                        'description':"If true module will output uppercase HELLO WORLD.",
                        'default':"False",
                        'required':"True",
                        'value':'False'
                },
        }

    def get_payload(self):
        if self.parameters["uppercase"]["value"].upper()=="TRUE":
            return "keyboard_write('HELLO WORLD');"
        else:
            return "keyboard_write('hello world');"

    def validate(self):
        if not is_bool(self.parameters['uppercase']['value']):
            return "Invalid value of uppercase - should be True or False"
        return ""

def init():
    return keyboard_hello_world()
 