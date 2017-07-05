from core.action import Action
from core.validators import *
from core.various import *
import collections

class keyboard_write(Action):

    mapping = {
        'ErrorRollOver'   : [0x01],
        'POSTFail'        : [0x02],
        'ErrorUndefined'  : [0x03],
        'a' : [0x04],
        'b' : [0x05],
        'c' : [0x06],
        'd' : [0x07],
        'e' : [0x08],
        'f' : [0x09],
        'g' : [0x0A],
        'h' : [0x0B],
        'i' : [0x0C],
        'j' : [0x0D],
        'k' : [0x0E],
        'l' : [0x0F],
        'm' : [0x10],
        'n' : [0x11],
        'o' : [0x12],
        'p' : [0x13],
        'q' : [0x14],
        'r' : [0x15],
        's' : [0x16],
        't' : [0x17],
        'u' : [0x18],
        'v' : [0x19],
        'w' : [0x1A],
        'x' : [0x1B],
        'y' : [0x1C],
        'z' : [0x1D],
        'A' : [0xE1, 0x04],
        'B' : [0xE1, 0x05],
        'C' : [0xE1, 0x06],
        'D' : [0xE1, 0x07],
        'E' : [0xE1, 0x08],
        'F' : [0xE1, 0x09],
        'G' : [0xE1, 0x0A],
        'H' : [0xE1, 0x0B],
        'I' : [0xE1, 0x0C],
        'J' : [0xE1, 0x0D],
        'K' : [0xE1, 0x0E],
        'L' : [0xE1, 0x0F],
        'M' : [0xE1, 0x10],
        'N' : [0xE1, 0x11],
        'O' : [0xE1, 0x12],
        'P' : [0xE1, 0x13],
        'Q' : [0xE1, 0x14],
        'R' : [0xE1, 0x15],
        'S' : [0xE1, 0x16],
        'T' : [0xE1, 0x17],
        'U' : [0xE1, 0x18],
        'V' : [0xE1, 0x19],
        'W' : [0xE1, 0x1A],
        'X' : [0xE1, 0x1B],
        'Y' : [0xE1, 0x1C],
        'Z' : [0xE1, 0x1D],
        '1' : [0x1E],
        '2' : [0x1F],
        '3' : [0x20],
        '4' : [0x21],
        '5' : [0x22],
        '6' : [0x23],
        '7' : [0x24],
        '8' : [0x25],
        '9' : [0x26],
        '0' : [0x27],
        '!' : [0xE1, 0x1E],
        '@' : [0xE1, 0x1F],
        '#' : [0xE1, 0x20],
        '$' : [0xE1, 0x21],
        '%' : [0xE1, 0x22],
        '^' : [0xE1, 0x23],
        '&' : [0xE1, 0x24],
        '*' : [0xE1, 0x25],
        '(' : [0xE1, 0x26],
        ')' : [0xE1, 0x27],
        'ENTER' : [0x28],
        'ESCAPE' : [0x29],
        'DELETE' : [0x2A],
        'Tab' : [0x2B],
        'Spacebar' : [0x2C],
        ' ' : [0x2C],
        '-' : [0x2D],
        '=' : [0x2E],
        '[' : [0x2F],
        ']' : [0x30],
        '\\' : [0x31],
        'NonUSHash' : [0x32],
        ';' : [0x33],
        '\'' : [0x34],
        'GraveAccent' : [0x35],
        ',' : [0x36],
        '.' : [0x37],
        '/' : [0x38],
        '_' : [0xE1, 0x2D],
        '+' : [0xE1, 0x2E],
        '{' : [0xE1, 0x2F],
        '}' : [0xE1, 0x30],
        '|' : [0xE1, 0x31],
        '~' : [0xE1, 0x32],
        ':' : [0xE1, 0x33],
        '"' : [0xE1, 0x34],
        'Tilde' : [0xE1, 0x35],
        '<' : [0xE1, 0x36],
        '>' : [0xE1, 0x37],
        '?' : [0xE1, 0x38],
        'CapsLock' : [0x39],
        'F1' : [0x3A],
        'F2' : [0x3B],
        'F3' : [0x3C],
        'F4' : [0x3D],
        'F5' : [0x3E],
        'F6' : [0x3F],
        'F7' : [0x40],
        'F8' : [0x41],
        'F9' : [0x42],
        'F10' : [0x43],
        'F11' : [0x44],
        'F12' : [0x45],
        'PrintScreen' : [0x46],
        'ScrollLock' : [0x47],
        'Pause' : [0x48],
        'Insert' : [0x49],
        'Home' : [0x4A],
        'PageUp' : [0x4B],
        'DeleteForward' : [0x4C],
        'End' : [0x4D],
        'PageDown' : [0x4E],
        'RightArrow' : [0x4F],
        'LeftArrow' : [0x50],
        'DownArrow' : [0x51],
        'UpArrow' : [0x52],
        'KeypadNumLock' : [0x53],
        'Clear' : [0xE1, 0x53],
        'KeypadSlash' : [0x54],
        'KeypadAsterisk' : [0x55],
        'KeypadMinus' : [0x56],
        'KeypadPlus' : [0x57],
        'KeypadENTER' : [0x58],
        'KeypadOne' : [0x59],
        'KeypadTwo' : [0x5A],
        'KeypadThree' : [0x5B],
        'KeypadFour' : [0x5C],
        'KeypadFive' : [0x5D],
        'KeypadSix' : [0x5E],
        'KeypadSeven' : [0x5F],
        'KeypadEight' : [0x60],
        'KeypadNine' : [0x61],
        'KeypadZero' : [0x62],
        'KeypadDot' : [0x63],
        'NonUSBackslash' : [0x64],
        'KeypadEnd' : [0x59],
        'KeypadDownArrow' : [0x5A],
        'KeypadPageDn' : [0x5B],
        'KeypadLeftArrow' : [0x5C],
        'KeypadRightArrow' : [0x5E],
        'KeypadHome' : [0x5F],
        'KeypadUpArrow' : [0x60],
        'KeypadPageUp' : [0x61],
        'KeypadInsert' : [0x62],
        'KeypadDelete' : [0x63],
        'NonUSPipe' : [0xE1, 0x64],
        'Application' : [0x65],
        'Power' : [0x66],
        'KeypadEqualSign' : [0x67],
        'F13' : [0x68],
        'F14' : [0x69],
        'F15' : [0x6A],
        'F16' : [0x6B],
        'F17' : [0x6C],
        'F18' : [0x6D],
        'F19' : [0x6E],
        'F20' : [0x6F],
        'F21' : [0x70],
        'F22' : [0x71],
        'F23' : [0x72],
        'F24' : [0x73],
        'Execute' : [0x74],
        'Help' : [0x75],
        'Menu' : [0x76],
        'Select' : [0x77],
        'Stop' : [0x78],
        'Again' : [0x79],
        'Undo' : [0x7A],
        'Cut' : [0x7B],
        'Copy' : [0x7C],
        'Paste' : [0x7D],
        'Find' : [0x7E],
        'Mute' : [0x7F],
        'VolumeUp' : [0x80],
        'VolumeDown' : [0x81],
        'LockingCapsLock' : [0x82],
        'LockingNumLock' : [0x83],
        'LockingScrollLock' : [0x84],
        'KeypadComma' : [0x85],
        'KeypadEqualSign' : [0x86],
        'International1' : [0x87],
        'International2' : [0x88],
        'International3' : [0x89],
        'International4' : [0x8A],
        'International5' : [0x8B],
        'International6' : [0x8C],
        'International7' : [0x8D],
        'International8' : [0x8E],
        'International9' : [0x8F],
        'LANG1' : [0x90],
        'LANG2' : [0x91],
        'LANG3' : [0x92],
        'LANG4' : [0x93],
        'LANG5' : [0x94],
        'LANG6' : [0x95],
        'LANG7' : [0x96],
        'LANG8' : [0x97],
        'LANG9' : [0x98],
        'AlternateErase' : [0x99],
        'SysReq' : [0x9A],
        'Cancel' : [0x9B],
        'Clear' : [0x9C],
        'Prior' : [0x9D],
        'Return' : [0x9E],
        'Separator' : [0x9F],
        'Out' : [0xA0],
        'Oper' : [0xA1],
        'ClearAgain' : [0xA2],
        'CrSelProps' : [0xA3],
        'ExSel' : [0xA4],
        'LeftControl' : [0xE0],
        'LeftShift' : [0xE1],
        'LeftAlt' : [0xE2],
        'LeftGUI' : [0xE3],
        'RightControl' : [0xE4],
        'RighShift' : [0xE5],
        'RightAlt' : [0xE6],
        'RightGUI' : [0xE7],
        }

    name = "keyboard_write"
    info = """keyboard_write is action that command device to simulate keyboard typing. 

keyboard_write takes as many arguments as device can process ;-) Normal text can be passed to
keyboard_write just as a string. 

Belowe payload will command device to simple output text Hello World! (with 0x0A character at end):

keyboard_write("Hello ","World!\\n");

There are some special keys - to emulate them you need to put them as argument for keyboard_write
(taken from HID Usage Tables @ www.usb.org):
%s
For examle below paylaod will just echo Hello Worl! like before but using one special key (BACKSPACE): 

    keyboard_write("Hellf", BACKSPACE, "o world!");

It's possible to use key combination like WINDOWS + R - just use operator. Below example will fire
windows console and execute exit command:

    keyboard_write(LeftGUI+"R","cmd.exe",ENTER,"EXIT", ENTER);

There is also function for developers - translate(self, payload). See source code for more information.

     """ % '\n'.join( sorted([ "- "+x for x in mapping if len(x)>1 ]) )

    short_description = """Command that simulate keyboard typing with selected device."""

    def validate(self, payload):
        for v in payload:
            if type(v)==list:
                for idx in range(0,len(v),2):
                    if idx+1<len(v) and v[idx+1]!='+':
                        return "Invalid operand %s in %s. See info action keyboard_write" % (v[idx+1],' '.join(v))
                    elif not payload_arg_is_string(v[idx]) and v[idx] not in [ x for x in self.mapping if len(x)>1 ]:
                        return "Invalid value, with + operand unknown special key (%s) - %s. See info action keyboard_write." % (v[idx],' '.join(v))
            elif not payload_arg_is_string(v) and v not in [ x for x in self.mapping if len(x)>1 ] :
                return "Uknown special key - %s. See info action keyboard_write." % v
        return ""

    def translate(self, payload):
        out = []
        for v in payload:
            if type(v)==list: # + operator used
                combo = [] 
                for idx in range(0,len(v),2):
                    if payload_arg_is_string(v[idx]):
                        for x in payload_arg_unquote(v[idx]):
                            combo = combo + self.mapping[x] 
                    else:
                        combo = combo + self.mapping[v[idx]]
                out.append(list(collections.OrderedDict.fromkeys(combo)))
            elif payload_arg_is_string(v): # string
                for c in payload_arg_unquote(v):
                    if len(self.mapping[c])==1:
                        out = out + self.mapping[c]
                    else:
                        out.append(self.mapping[c])
            else: # SPECIAL KEY
                if len(self.mapping[v])==1:
                    out = out + self.mapping[v]
                else:
                    out.append(self.mapping[v])
        return out
    def __str__(self):
        return self.name

def init():
        return keyboard_write()


