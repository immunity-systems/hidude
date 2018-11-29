__author__ = "Karol Celinski"
__copyright__ = "Copyright 2017, Immunity Systems Sp. z o.o."
__credits__ = ["Andrzej Nowodworski", "Pawel Maziarz"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Karol Celinski"
__email__ = "karolc@immunity-systems.com"

from core.module import Module
from core.action_manager import action_manager
from core.validators import *
from core.various import *

class hid_mouse(Module):
        name = "hid_mouse"
        short_description = "Turns device into HID mouse that spoof moves, clicks based on const payload after plugin"
        payload_actions = ["sleep", "mouse_move", "mouse_click", "mouse_scroll"]
        payload_description = "In payload you can use %s " % " ".join(payload_actions)
        description = " ".join([short_description, payload_description])
        required_actions = payload_actions + ["program"] 
        parameters = {
                'sleep_enabled': {
                        'description':"Does device have to sleep before start after power on.",
                        'default':"True",
                        'required':"True",
                },
                'sleep_time': {
                        'description':"Number of miliseconds to sleep.",
                        'default':"10",
                        'required':"True",
                }

        }

        def validate(self):
                err = ""
                if not is_bool(self.parameters['sleep_enabled']['value'].upper()):
                        err=err+"Invalid value of sleep_enabled - should be True or False"
                if not is_number(self.parameters['sleep_time']['value'],True):
                        return "Invalid value of sleep_time - must be positive number!"
                actions = action_manager.parse_payload(self.payload)
                #module custom validation
                for command in actions:
                        if command['action'] not in self.required_actions:
                                return "Invalid value of payload - unknown action - %s !" % command['action']
                #action validation
                return action_manager.validate_actions(actions)

        def execute(self, payload, device):
                """
                It's executed after all parameters all set.
                """
                if self.parameters['sleep_enabled']['value'].upper()=="TRUE":
                        payload = ("sleep(%i);"% int(self.parameters['sleep_time']['value']) ) + payload
                parsed_payload = action_manager.parse_payload(payload)
                device_input = None
                print_info("Processing payload")
                for command in parsed_payload:
                        processed = device.perform_action(command['action'], command['arguments'])
                        if device_input == None:
                                device_input = processed
                        else:
                                device_input = device_input + processed
                print_info("Payload ready. Let's program device !")
                out = device.perform_action("program",device_input)
                return out


def init():
        return hid_mouse()
