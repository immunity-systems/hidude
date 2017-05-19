__author__ = "Pawel Maziarz"
__copyright__ = "Copyright 2017, Immunity Systems Sp. z o.o."
__credits__ = ["Andrzej Nowodworski", "Karol Celinski"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Pawel Maziarz"
__email__ = "pawelm@immunity-systems.com"

from core.device import Device
import time
from core.various import *
from core import various
from core.validators import *
import os
from core.action_manager import action_manager
import struct
import urllib2
import sys

class EspusbWS(Device):
    name = "EspusbWS"
    short_description = "Espusb ESP8266 USB Software Driver - Web Sockets"
    info = """
    Espusb is proof of concept of software USB on ESP8266/ESP8285 (wifi 
    enabled) microcontrollers. Hardware design requires only one external 
    resistor between D- and 3.3V. 

    This device utilizes espusb websockets endpoint. You have to be on 
    the same network and espusb device must be reachable (typical it's 
    at 192.168.4.1). The payload is executed immediately via WiFi.

    Espusb website: https://github.com/cnlohr/espusb
    """ 
    dev_info = None
    dev = None
    parameters = {
                'ip_address': {
                        'description':"Ip address of a device (typicaly 192.168.4.1)",
                        'default':"True",
                        'required':"True",
                        'value':"192.168.4.1"
                }
        }

    def validate(self):
        if not self.parameters['ip_address']['value']:
            # XXX - valid ip validation
            return "Invalid value of ip_address - should be an IP address"
        return ""

    def action_program(self, input):
        raw=""
        for command in input:
           if command['type'] == "keyboard_write":
                raw = action_manager.actions["keyboard_write"].translate(command['input'])
                self.send_keys(raw)
           elif command['type'] == "sleep":
                pass
           elif command['type'] == "mouse_move":
                return ("mouse_move: Not implemented yet", None)
                pass
           else:
                return ("Unknown action occured during firmware patch !", None)

        return ""

    def send_keys(self, keys):
        various.print_info("Sending keys...")
        errcount = 0
        successcount = 0
        for key in keys:
            modifiers = 0 # TODO
            r0 = urllib2.urlopen("http://%s/d/issue?CK%d%%09%d" % (self.parameters['ip_address']['value'], modifiers, key)).read()
            r1 = urllib2.urlopen("http://%s/d/issue?CK%d%%09%d" % (self.parameters['ip_address']['value'], modifiers, 0)).read()
            if r0 == "CK":
                successcount = successcount + 1
            else:
                errcount = errcount + 1
        various.print_info("Done (success chars=%d, error chars=%d)" % (successcount, errcount))

    def action_keyboard_write(self, input):
        return [ { "type" : "keyboard_write", "input": input } ]
 
    def action_mouse_move(self, input):
        return [ { "type" : "mouse_move", "move":input} ]
 
    def action_sleep(self, input):
        return [ { "type" : "sleep", "time":input} ]

    def dependency_check(self):
        try:
            import urllib2
        except Exception as e:
            return str(e)
        return ""

def init():
    return EspusbWS()
