from device import Device
from payload import Payload
import consts
import sys
import traceback
import various
import os
import time
from pyparsing import Word, alphas, alphanums, oneOf, OneOrMore, \
        commaSeparatedList, Suppress, Forward, Group, Optional, \
        delimitedList, Regex, operatorPrecedence, opAssoc, quotedString, \
        dblQuotedString, Literal, QuotedString, infixNotation


action_manager = None

class ActionManager:
    devices = []
    actions_map = {}
    device_map =  {}
    actions = {}
 
    def __init__(self):
        for action in os.listdir(os.path.dirname(os.path.abspath(__file__))+"/"+consts.actions_dir):
                if action == '__init__.py' or action[-3:] != '.py':
                        continue
                try:
                        act = __import__(consts.core_dir+"."+consts.actions_dir+"."+action[:-3], locals(), globals(),action[:-3])
                        a = act.init()
                        self.actions[a.name] = a
                except:
                        print "!) Error loading '%s' action ! " % action
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60
                        time.sleep(1)

    """
    Get devices that provide required actions
    """
    def get_supported_devices(self,required_actions):
        possible_devices = self.devices
        for r in required_actions:
            if r not in self.actions_map:
                return []
            possible_devices = list(set(self.actions_map[r]).intersection(possible_devices))
        return possible_devices

    """
    Add new device to supported list if error occure return error message
    """
    def register_device(self,device):
        try:
            device.dependency_check()
        except e:
            return str(e)
        abils = device.get_actions()
        self.devices.append(device)
        for a in abils:
            if a not in self.actions:
                various.print_warning("Device register not supported acction - %s!" % a)
            if not a in self.actions_map:
                self.actions_map[a]=[]
            self.actions_map[a].append(device)
        self.device_map[str(device)] = device
        return ""

    """
    Filter modules supported by device or payload
    """
    def filter_supported_modules(self, obj, module_list):
        out = []
        if isinstance(obj,Device):
            device = obj
            for m in module_list:
                if device in self.get_supported_devices(module_list[m].required_actions):
                    out.append(m)
        elif isinstance(obj,Payload):
            payload = obj
            for m in module_list:
                if set(module_list[m].payload_actions)==set(payload.satisfied_actions):
                    out.append(m)
        else:
            out = []
        return out

    """
    Return all devices
    """
    def get_all_devices(self):
        return self.devices

    """
    Return all devices names
    """
    def get_all_devices_str(self):
        return [ str(x) for x in self.devices ]

    """
    Parse payload from string and return list of dicts
    """
    def parse_payload(self,payload):
        expr = Forward()
        
        LPAR, RPAR, SEMI = map(Suppress, "();")
        identifier = Word(alphas+"_", alphanums+"_")
        function_call = identifier.setResultsName("name") + LPAR + Group(Optional(delimitedList(expr))) + RPAR
        integer = Regex(r"-?\d+")
        real = Regex(r"-?\d+\.\d*")
        
        qstr = QuotedString(quoteChar = '"', escChar = '\\', unquoteResults=False)
        qstrsingle = QuotedString(quoteChar = "'", escChar = '\\', unquoteResults=False)
        operand = (identifier | real | integer | qstr | qstrsingle )
        plusop = oneOf('+ -')
        expr << infixNotation( operand, [ (plusop, 2, opAssoc.LEFT) ])
        out = []
        for t,s,e in function_call.scanString( payload ):
                out.append({
                                "action" : t[0],
                                "arguments" : t[1].asList() if type(t[1])!=str else t[1] 
                           }
                          )
        return out

    """
    Validate parsed payload. If error return message else return ""
    """
    def validate_actions(self,actions):
        for command in actions:
                action = command["action"]
                value  = command["arguments"]
                if action not in self.actions:
                     return "Action %s - unknown action!" % action
                e = self.actions[action].validate(value)
                if e!="":
                         return e
        return ""
    
if action_manager is None:
    action_manager = ActionManager()
