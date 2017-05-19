__author__ = "Karol Celinski"
__copyright__ = "Copyright 2017, Immunity Systems Sp. z o.o."
__credits__ = ["Andrzej Nowodworski", "Pawel Maziarz"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Karol Celinski"
__email__ = "karolc@immunity-systems.com"

from core.payload import Payload
from core.validators import *
import os

class rubberduck_payload(Payload):
    name = "rubberduck_payload"
    info = """This payload get as input filename (parameter input_filename) with rubberduck payload and
convert it to Hi-Dude format. Optionaly if parameter save_output is set to true, converted payload will be
also saved in file specified in out_filename. 
    """
    short_description = "Yeah - you can use any rubberduck payload ;-)."
    satisfied_actions = ['keyboard_write', 'sleep']
    parameters = {
                'input_filename': {
                        'description':"File to convert.",
                        'default':"",
                        'required':"True",
                        'value':''
                },
                'save_output': {
                        'description':"If true converted payload will be saved.",
                        'default':"False",
                        'required':"True",
                        'value':'False'
                },
                 'out_filename': {
                        'description':"Filename to save output file if save_output = True.",
                        'default':"",
                        'required':"True",
                        'value':''
                },
                'dont_program': {
                        'description':"If set to True device will not be programmed (helpful when you want only save converted file).",
                        'default':"False",
                        'required':"True",
                        'value':'False'
                },
 
        }
    default_delay = 0 
    mapping = {
        'F1' : 'F1',
        'F2' : 'F2',
        'F3' : 'F3',
        'F4' : 'F4',
        'F5' : 'F5',
        'F6' : 'F6',
        'F7' : 'F7',
        'F8' : 'F8',
        'F9' : 'F9',
        'F10' : 'F10',
        'F11' : 'F11',
        'F12' : 'F12',
        'WINDOWS' : 'LeftGUI',
        'GUI' : 'LeftGUI',
        'MENU' : 'Application',
        'APP' : 'Application',
        'SHIFT' : 'LeftShift',
        'ALT' : 'LeftAlt',
        'ENTER' : 'ENTER',
        'CONTROL' : 'LeftControl',
        'CTRL' : 'LeftControl',
        'DOWNARROW':'DownArrow',
        'DOWN':'DownArrow',
        'LEFTARROW':'LeftArrow',
        'LEFT':'LeftArrow',
        'RIGHTARROW':'RightArrow',
        'RIGHT':'RightArrow',
        'UPARROW':'UpArrow',
        'UP':'UpArrow',
        'BREAK':'Pause',
        'PAUSE':'Pause',
        'CAPSLOCK':'CapsLock',
        'DELETE':'DeleteForward',
        'END':'End',	
        'ESC':'ESCAPE',
        'ESCAPE':'ESCAPE',
        'HOME':'Home',
        'INSERT':'Insert',
        'NUMLOCK':'LockingNumLock',
        'PAGEUP':'PageUp',
        'PAGEDOWN':'PageDown',
        'PRINTSCREEN':'PrintScreen',
        'SCROLLLOCK':'ScrollLock',
        'SPACE':'" "',
        'TAB':'Tab',
    }

    def do_execute(self):
        return self.parameters['dont_program']['value'].upper()=="FALSE"

    def get_payload(self):
        payload = ""
        with open(self.parameters['input_filename']['value'], "r") as ins:
            for line in ins:
                ln = line.split(' ')
                if ln[0].rstrip() in self.mapping.keys():
                    out = ""
                    for x in ln:
                        if x.rstrip() in self.mapping.keys():
                            if out == "":   
                                out=self.mapping[x.rstrip()]
                            else:
                                out=out+"+" + self.mapping[x.rstrip()]
                        else:
                            out = out+'%s"%s"' % ("+" if out!="" else "",x.rstrip())
                    payload = payload + "keyboard_write(%s);\n" % out
                elif ln[0]=="REM":
                    pass
                elif ln[0] in ["DEFAULT_DELAY", "DEFAULTDELAY"] and is_number(ln[1],True):
                    self.default_delay = int(ln[1])
                elif ln[0]=="DELAY":
                    payload = payload + "sleep(%s);\n" % ln[1].rstrip()
                elif ln[0]=="STRING":
                    payload = payload + 'keyboard_write("%s");\n' % ' '.join(ln[1:]).rstrip().replace('"','\\"')
        if self.parameters["save_output"]["value"].upper()=="TRUE":
            f = open(self.parameters['out_filename']['value'], "w")
            f.write(payload)
            f.close()
        return payload

    def validate(self):
        if not is_bool(self.parameters['save_output']['value']):
            return "Invalid value of save_output - should be True or False"
        if not is_bool(self.parameters['dont_program']['value']):
            return "Invalid value of dont_program - should be True or False"
        if self.parameters['save_output']['value'].upper()=="TRUE" and\
           self.parameters['input_filename']['value']=="":
            return "Please set input_filenam"
        if self.parameters['save_output']['value'].upper()=="TRUE" and\
           self.parameters['out_filename']['value']=="":
            return "Please set out_filename"
        if not is_bool(self.parameters['save_output']['value']):
            return "Invalid value of save_output - should be True or False"
        if not os.path.isfile(self.parameters['input_filename']['value']):
            return "Check input_filename - bad path or not file "
        try:
            f = open(self.parameters['out_filename']['value'],"w")
            f.close()
        except:
            return "Unable to open file for saving output - check out_filename."
        return ""

def init():
    return rubberduck_payload()
 