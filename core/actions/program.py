from core.action import Action
from core.validators import *

class program(Action):
    name = "program"
    info = """This action can't be used in payload. It's only for marking programming ability in device.

Pragramatic usage is simple, as argument program takes added results of other actions invoked in device.
For example if you want to program device to write Hello World you should use this python code
(assuming that device is set to device that support keyboard_write and program:

        parsed_payload = action_manager.parse_payload('keyboard_write("Hello World");')
        device_input = None
        print_info("Processing payload")
        for command in parsed_payload:
                processed = device.perform_action(command['action'], command['arguments'])
                if device_input == None:
                        device_input = processed
                else:
                        #adding results of all actions in payload
                        device_input = device_input + processed
        # and programming ...
        out = device.perform_action("program",device_input)

    """
    short_description = """Programming ability of device. Not for payload."""

    def validate(self, payload):
           return "Error - program can't be used in payload!"

    def __str__(self):
        return self.name

def init():
        return program()

