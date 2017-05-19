from cmd2 import Cmd, options, make_option, USE_ARG_LIST
from core import consts
import cmd2
from core.action_manager import action_manager
import time
from core import various
import os
import sys
import cmd
import traceback

#drg############################################################3
# do posprzatania - ten kod naprawia tab completion na macu, a nie zauwazylem, zeby psul linuxy
import readline
import rlcompleter

if 'libedit' in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")
#drg############################################################3

class HID(Cmd):
    prompt = Cmd().colorize("HID > ","green")
    intro = Cmd().colorize(consts.logo1,"blue") + Cmd().colorize(consts.logo2,"red")
    current_parameters = {"module":[], "device":[], "payload":[]}
    payload = ""
    modules = {}
    payloads = {}
    active_module = active_payload = active_device = None 
    ruler = ''
    doc_header = "to be initialized"
    multilineCommands = ['payload']
    terminators = []
    important_commands = [
                                'do_list_devices', 
                                'do_list_modules', 
                                'do_list_payloads',
                                'do_list_actions', 
                                'do_info', 
                                'do_use', 
                                'do_show', 
                                'do_execute',
                                'do_payload'
                          ]

    def default(self, line):
            self.stdout.write('*** Unknown syntax: %s\n'%line)
            self.stdout.write("Type 'help'\n")

    def do_execute(self, line):
            """Execute module. To use commend first use module, device and set payload !

    Usage: just type execute and voilla!
            """
            if self.active_module == None or \
               ( self.active_payload == None and not self.modules[self.active_module].payload_custom ) or \
               (self.active_device==None and self.modules[self.active_module].require_device()):
                        various.print_warning("Please set all components before executing. See help use")
                        return
            dev = action_manager.device_map[self.active_device]
            mod = self.modules[self.active_module]
            if self.modules[self.active_module].payload_custom:
                    pay = None
            else:
                    pay = self.payloads[self.active_payload]
            e=dev.validate()
            if e!="":
                various.print_warning("Validation error in device: %s" % e)
                return
            if not self.modules[self.active_module].payload_custom:
                e = pay.validate()
            if pay != None and e!="":
                various.print_warning("Validation error in payload: %s" % e)
                return
            # payload and device is ready let's set payload and make validation
            if not self.modules[self.active_module].payload_custom:
                pay_c = pay.get_payload()
                mod.payload = pay_c
            else:
                pay_c = self.modules[self.active_module].payload
            # and validate  in module
            e = mod.validate()
            if e!="":
                various.print_warning("Validation error in module: %s" % e)
                return
            if self.modules[self.active_module].payload_custom or\
               pay.do_execute():
                  e = mod.execute(pay_c, dev)
            if e!="":
                various.print_warning("Error executing module: %s" % e)
                return

    def do_help(self, arg):
            """List available commands with "help" or detailed help with "help cmd"."""
            tmp = self.get_names
            self.get_names = self.get_names_hack # Ugly hack: I'm to lazy to reimplement whole do_help ;-)
            Cmd.do_help(self,arg)
            self.get_names = tmp
            if arg == "":
                self.print_topics(
                                "\n[ "+various.colorize("red","Important commands")+" ]\n", 
                                [ x[3:] for x in self.important_commands ], 
                                15, 
                                80
                             )
                print "\n[ "+various.colorize("red","Example usage")+" ]\n"+consts.example_usage
    def get_names_hack(self):
            names = Cmd.get_names(self)
            return list(set(names).difference(set(self.important_commands)))

    @options([make_option('-l', '--long', action="store_true", help="describe function of parameter")])
    def do_show(self, arg, opts):
        """        Shows value of a parameter.
Usage: show [options] arg

Options:
  -h, --help  show this help message and exit
  -l, --long  describe function of parameter

        """
        if USE_ARG_LIST:
            if arg:
                arg = arg[0]
            else:
                arg = ''

        param = arg.strip().lower()
        result = {}
        result_special = { "module":{},"device":{},"payload":{} }
        maxlen = 0
        for p in self.settable:
            if (not param) or p.startswith(param):
                skip = False
                for param_type in self.current_parameters:
                        if p in self.current_parameters[param_type]:
                               if p == "payload":
                                        extra = " ("+various.colorize("green", ( "custom" if self.modules[self.active_module].payload_custom else "loaded"))+")"
                                        if self.modules[self.active_module].payload_custom:
                                                result_special[param_type][p] = '%s%s\n--------------------------- # Payload value\n%s\n---------------------------' % ( p, extra, str( getattr(self, p) ) )
                               else:
                                        extra=""
                                        maxlen = max(maxlen, len(various.strip_escape('%s%s: %s' % ( p, extra, str( getattr(self, p) ) ))))
                                        result_special[param_type][p] = '%s%s: %s' % ( p, extra, str( getattr(self, p) ) )
                               skip=True
                if skip:
                        continue
                result[p] = '%s: %s' % (p, str(getattr(self, p)))
                maxlen = max(maxlen, len(various.strip_escape('%s: %s' % (p, str(getattr(self, p))))))
        if result:
            print "\n[ "+various.colorize("red","GLOBAL PARAMETERS")+" ]\n"
            for p in sorted(result):
                if opts.long:
                    #ljust dont work properly with ansi escape :-(
                    self.poutput('%s%s # %s' % (
                                                  result[p],
                                                  " "*(maxlen-len(various.strip_escape(result[p]))),
                                                  self.settable[p]
                                               )
                                )
                else:
                    self.poutput(result[p])
        was_special = False
        for param_type in result_special:
                if result_special[param_type]:
                        was_special = True
                        print "\n[ "+various.colorize("red",param_type.upper()+" PARAMETERS")+" ]\n"
                        for p in sorted(result_special[param_type]):
                                if opts.long:
                                        if param_type=="module":
                                                doc = self.modules[self.active_module].parameters[p]['description'] if p!="payload" else "See \"info parameter payload\" "
                                        elif param_type=="device":
                                                doc = action_manager.device_map[self.active_device].parameters[p]['description'] 
                                        elif param_type=="payload":
                                                doc = self.payloads[self.active_payload].parameters[p]['description'] 
                                        #ljust dont work properly with ansi escape :-(
                                        self.poutput('%s%s # %s' % (
                                                                   result_special[param_type][p],
                                                                   " "*(maxlen-len(various.strip_escape(result_special[param_type][p]))),
                                                                   doc
                                                                 )
                                                    )
                                else:
                                        self.poutput(result_special[param_type][p])

        if not (result or was_special):
            raise LookupError("Parameter '%s' not supported (type 'show' for list of parameters)." % param)
        else:
            print "\n"

    def do_payload(self,line):
        """Sets a payload.
               Just type: 
                        set payload
                And then line by line your payload. Empty new line finish payload
        """
        self.payload = line
        self.modules[self.active_module].payload = self.payload
        self.modules[self.active_module].payload_custom=True
        self.prompt = Cmd().colorize("HID [","green")+ \
                Cmd().colorize(self.active_module,"red")+ \
                "("+\
                ( Cmd().colorize("custom","blue") if self.modules[self.active_module].payload_custom else Cmd().colorize(self.active_payload,"blue"))+\
                ")"+ \
                (" @ "+Cmd().colorize(self.active_device,"red") if self.active_device!=None else "")+ \
                Cmd().colorize("] > ","green")
        various.print_info("Payload set!")


    def do_set(self,line):
        """Sets a settable parameter.

                Accepts abbreviated parameter names so long as there is no ambiguity.
                Call without arguments for a list of settable parameters with their values.
                Command can be used to set parameter of active module, payload, device or 
                global options.
                
                To set custom payload see help payload: 
        """
        out = Cmd.do_set(self,line)
        if len(line.split())>=2:
                pname = line.split()[0]
                pvalue = line.split()[1]
                if pname=="payload":
                        self.modules[self.active_module].payload = self.payload
                        self.modules[self.active_module].payload_custom=True
                        self.prompt = Cmd().colorize("HID [","green")+ \
                                Cmd().colorize(self.active_module,"red")+ \
                                "("+\
                                ( Cmd().colorize("custom","blue") if self.modules[self.active_module].payload_custom else Cmd().colorize(self.active_payload,"blue"))+\
                                ")"+ \
                                (" @ "+Cmd().colorize(self.active_device,"red") if self.active_device!=None else "")+ \
                                Cmd().colorize("] > ","green")

                elif pname in self.current_parameters["module"]:
                        self.modules[self.active_module].parameters[pname]["value"] = getattr(self, pname)
                elif pname in self.current_parameters["device"]:
                        action_manager.device_map[self.active_device].parameters[pname]["value"] = getattr(self, pname)
                elif pname in self.current_parameters["payload"]:
                        self.payloads[self.active_payload].parameters[pname]["value"] = getattr(self, pname)
        return out

    def complete_set(self, text, line, begidx, endidx):
        mapping = {}
        for p in self.settable:
                mapping[p]=[]
        return self.option_argument_complete(text, line, begidx, endidx, mapping)


    def use_module(self,line):
        self.active_module = line.split()[1]
        self.active_payload = self.active_device = None
        # clear all settables
        for param_type in self.current_parameters:
                for x in self.current_parameters[param_type]:
                        Cmd.settable.pop(x)
        if len(self.modules[self.active_module].payload_actions)>0:
                self.current_parameters = {"module":["payload"], "device":[], "payload":[]}
                if "payload" not in Cmd.settable:
                        Cmd.settable.append("payload")
                #initialize parameters and payload
                if getattr(self.modules[self.active_module], "payload", None) is None:
                        self.modules[self.active_module].payload=""
                        self.modules[self.active_module].payload_custom=True
                self.payload = self.modules[self.active_module].payload
        else:
                self.current_parameters = {"module":[], "device":[], "payload":[]}

        for name,p in self.modules[self.active_module].parameters.iteritems():
                if "value" not in p:
                        p["value"]=p["default"]
                setattr(self,name,p["value"])
                self.current_parameters["module"].append(name)
                Cmd.settable.append(name)
        if not self.modules[self.active_module].payload_custom:
                self.use_payload("payload "+self.modules[self.active_module].loaded_payload)
        self.prompt = Cmd().colorize("HID [","green")+ \
                      Cmd().colorize(self.active_module,"red")+ \
                      "("+\
                      ( Cmd().colorize("custom","blue") if self.modules[self.active_module].payload_custom else Cmd().colorize(self.active_payload,"blue"))+\
                      ")"+ \
                      (" @ "+Cmd().colorize(self.active_device,"red") if self.active_device!=None else "")+ \
                      Cmd().colorize("] > ","green")


    def use_device(self,line):
        if not action_manager.filter_supported_modules( 
                                                   action_manager.device_map[line.split()[1]], 
                                                   { self.active_module:self.modules[self.active_module] }
                                                 ):
                various.print_warning("device not supporting selected module")
                return
        self.active_device = line.split()[1]
        # clear settables
        for x in self.current_parameters["device"]:
                Cmd.settable.pop(x)
        self.current_parameters["device"] = []
        for name,p in action_manager.device_map[self.active_device].parameters.iteritems():
                if "value" not in p:
                        p["value"]=p["default"]
                setattr(self,name,p["value"])
                self.current_parameters["device"].append(name)
                Cmd.settable.append(name)

        self.prompt = Cmd().colorize("HID [","green")+ \
                      Cmd().colorize(self.active_module,"red")+ \
                      ( "("+Cmd().colorize(self.active_payload,"blue")+")" if self.active_payload!=None else "")+ \
                      " @ "+ \
                      Cmd().colorize(self.active_device,"red")+ \
                      Cmd().colorize("] > ","green")

    def use_payload(self,line):
        if not action_manager.filter_supported_modules( self.payloads[line.split()[1]], 
                                                  { self.active_module:self.modules[self.active_module] } 
                                                 ):
                various.print_warning("payload not supporting selected module")
                return
        self.active_payload = line.split()[1]
        # clear settables
        for x in self.current_parameters["payload"]:
                Cmd.settable.pop(x)
        self.current_parameters["payload"] = []
        for name,p in self.payloads[self.active_payload].parameters.iteritems():
                if "value" not in p:
                        p["value"]=p["default"]
                setattr(self,name,p["value"])
                self.current_parameters["payload"].append(name)
                Cmd.settable.append(name)
        self.modules[self.active_module].loaded_payload=line.split()[1]
        self.prompt = Cmd().colorize("HID [","green")+ \
                      Cmd().colorize(self.active_module,"red")+ \
                      "("+Cmd().colorize(self.active_payload,"blue")+")"+ \
                      (" @ "+Cmd().colorize(self.active_device,"red") if self.active_device!=None else "")+ \
                      Cmd().colorize("] > ","green")
        self.modules[self.active_module].payload_custom = False

    def do_use(self,line):
        """Activate selected module, payload or device.

    Usage: 
        use module <module name> 
        use device <device name> - only when module is selected!
        use payload <payload name> - only when module is selected!
    Please use TAB for completion.
        """
        if len(line.split())<2 or line.split()[0] not in ["module", "device", "payload"]:
                various.print_warning("invalid syntax - try help use")
                return
        if line.split()[0]=="module" and line.split()[1] not in self.modules:
                various.print_warning("%s unknown module" % line.split()[1])
                return 
        elif line.split()[0]=="device" and line.split()[1] not in action_manager.get_all_devices_str():
                various.print_warning("%s unknown device" % line.split()[1])
                return 
        elif line.split()[0]=="payload" and line.split()[1] not in self.payloads:
                various.print_warning("%s unknown payload" % line.split()[1])
                return 
        elif line.split()[0] in ["device", "payload"] and self.active_module is None:
                various.print_warning("First select module!")
                return 
        if line.split()[0]=="module":
                self.use_module(line)
        elif line.split()[0]=="device":
                self.use_device(line)
        elif line.split()[0]=="payload":
                self.use_payload(line)

    def complete_use(self, text, line, begidx, endidx):
        mapping = {
                "device" : action_manager.get_all_devices_str(),
                "module" : [ str(v) for k,v in self.modules.iteritems() ],
                "payload" : [ str(v) for k,v in self.payloads.iteritems() ],
        }
        return self.option_argument_complete(text, line, begidx, endidx, mapping)

    def info_module(self,arg):
        if arg == None and self.active_module != None:
                arg = self.active_module
        if arg not in self.modules:
                various.print_warning("%s - unknown module" % arg)
                return 
        print "\n=[ MODULE "+various.colorize("red",arg)+" ]=\n"
        print "Required actions:"
        for x in self.modules[arg].required_actions:
                print "- %s" % x
        print "\n[ "+various.colorize("red","INFO")+" ] \n"
        print self.modules[arg].short_description
        print "\n"
        print "[ "+various.colorize("red","DESCRIPTION")+" ] \n"
        print self.modules[arg].description
        print "\n"
        print "[ "+various.colorize("red","PARAMETERS")+" ] \n"
        for x in self.modules[arg].parameters:
                p = self.modules[arg].parameters[x]
                print "- %s = %s : (default value \"%s\") parameter is %srequired" % (x,p["value"],p["default"], ("" if p["required"] else "not "))
        print "\nFor detail info about parameter in activate module (with use command) and type: info parameter NAME\n"
        print "[ "+various.colorize("red","PAYLOAD")+" ] \n"
        print "Payload type: "+various.colorize("green","custom" if self.modules[self.active_module].payload_custom else "loaded")
        print "Payload actions:"
        for x in self.modules[arg].payload_actions:
                print "- %s" % x
        if not self.modules[self.active_module].payload_custom:
                print "Payload name: %s" % various.colorize("blue",self.active_payload)
        else:
                print "Payload value\n---------------------------\n%s\n---------------------------\n" % various.colorize("blue",self.payload) 
        print "\n"

    def info_action(self,arg):
        if arg not in action_manager.actions:
                various.print_warning("%s - unknown action" % arg)
                return 
        print "\n=[ ACTION "+various.colorize("red",arg)+" ]=\n"
        print "\n[ "+various.colorize("red","INFO")+" ] \n"
        print action_manager.actions[arg].short_description
        print "\n"
        print "[ "+various.colorize("red","DESCRIPTION")+" ] \n"
        print action_manager.actions[arg].info


    def info_parameter(self,arg):
        if self.active_module is None:
                various.print_warning("First you need to activate module with use command!")
                return 
        if arg not in self.modules[self.active_module].parameters and \
           not self.modules[self.active_module].payload_custom and arg not in self.payloads[self.active_payload].parameters and \
           arg not in action_manager.device_map[self.active_device].parameters and \
           (arg!="payload" or len(self.modules[self.active_module].payload_actions)==0):
                various.print_warning("%s - unknown parameter" % arg)
                return 
        if arg!="payload":
                if arg in self.modules[self.active_module].parameters:
                        p = self.modules[self.active_module].parameters[arg]
                elif not self.modules[self.active_module].payload_custom and arg in self.payloads[self.active_payload].parameters:
                        p = self.payloads[self.active_payload].parameters[arg]
                elif arg in action_manager.device_map[self.active_device].parameters:
                        p = action_manager.device_map[self.active_device].parameters[arg]
        print "\n[ PARAMETER "+various.colorize("red",arg)+" ]\n"
        print "Required: " + various.colorize("blue","True" if (arg=="payload" or p["required"]) else "False")
        if arg!="payload":
                print "Default value: " + various.colorize("blue",p["default"])
        print "Value: " + various.colorize("blue",self.payload if arg=="payload" else p["value"])
        print "\n"
        print ( self.modules[self.active_module].payload_description if arg=="payload" else p["description"])+"\n"

    def info_device(self,arg):
        if arg == None and self.active_device != None:
                arg = self.active_device
        if arg not in action_manager.device_map:
                various.print_warning("%s - unknown device" % arg)
                return 
        print "\n=[ DEVICE "+various.colorize("red",arg)+" ]=\n"
        dev = action_manager.device_map[arg]
        print "Provided actions:"
        for x in dev.get_actions():
                print "- %s" % x
        print "\n[ "+various.colorize("red","INFO")+" ] \n"
        print dev.info
        print "\n"
        print "[ "+various.colorize("red","PARAMETERS")+" ] \n"
        for k,p in action_manager.device_map[arg].parameters.iteritems():
                print "- %s = %s : (default value \"%s\") parameter is %srequired" % (k,p["value"],p["default"], ("" if p["required"] else "not "))
        print "\nFor detail info about parameter in activate module (with use command) and type: info parameter NAME\n"

    def info_payload(self,arg):
        if arg == None and self.active_payload != None:
                arg = self.active_payload
        if arg not in self.payloads:
                various.print_warning("%s - unknown payload" % arg)
                return 
        print "\n=[ PAYLOAD "+various.colorize("red",arg)+" ]=\n"
        pay = self.payloads[arg]
        print "Satisfied actions:"
        for x in pay.satisfied_actions:
                print "- %s" % x
        print "\n[ "+various.colorize("red","DESCRIPTION")+" ] \n"
        print pay.short_description+"\n"
        print pay.info
        print "[ "+various.colorize("red","PARAMETERS")+" ] \n"
        for k,p in self.payloads[arg].parameters.iteritems():
                print "- %s = %s : (default value \"%s\") parameter is %srequired" % (k,p["value"],p["default"], ("" if p["required"] else "not "))
        print "\nFor detail info about parameter in activate module (with use command) and type: info parameter NAME\n"

    def do_info(self,line):
        """Print information about components.

    Usage: info [COMPONENT ARGUMENT]
    Where  COMPONENT is one of module, device, payload, parameter.

    Syntax:
    * info - print info about active module, device and payload.
    * info device [DEVICE_NAME] - print info about device (submitted as argument or active).
    * info module [MODULE_NAME] - print info about module (submitted as argument or active).
    * info payload [PAYLOAD_NAME] - print info about payload (submitted as argument or active).
    * info action [ACTION_NAME] - print info about action (see list_actions for available names).
    * info parameter OPTION_NAME - print info about parameter in active module, payload or device.

        """
        if len(line.split())<2 and (len(line.split())!=0 and self.active_module is None):
                various.print_warning("invalid syntax - try help info")
                return
        if len(line.split())!=0 and line.split()[0] not in ["device","module","payload","parameter","action"]:
                various.print_warning("invalid syntax - try help info")
                return
        if len(line.split())==0:
                self.info_module(self.active_module)
                if(self.active_device!=None):
                        self.info_device(None)
                if(self.active_payload!=None):
                        self.info_payload(None)
        else:
                getattr(self,"info_"+line.split()[0])(line.split()[1] if len(line.split())>1 else None)

    def complete_info(self, text, line, begidx, endidx):
        mapping = {
                "device" : action_manager.get_all_devices_str(),
                "module" : [ str(v) for k,v in self.modules.iteritems() ],
                "payload" : [ str(v) for k,v in self.payloads.iteritems() ],
                "action" : action_manager.actions.keys(), 
                "parameter" : self.current_parameters["module"] +\
                              self.current_parameters["device"] +\
                              self.current_parameters["payload"]
        }
        return self.option_argument_complete(text, line, begidx, endidx, mapping)

    def option_argument_complete(self, text, line, begidx, endidx, option_arguments_map):
        opts = option_arguments_map.keys()
        if (len(line.split())==3 or ( len(line.split())==2 and line[-1:]==" ")) and line.split()[1] in opts:
                useopts = []
                for opt in option_arguments_map:
                        if line.split()[1]==opt:
                                useopts = option_arguments_map[opt]
                if not text:
                        completions = useopts[:]
                else:
                        completions = [ f for f in useopts if f.startswith(text) ]
                return completions
        elif len(line.split())==2:
                out = []
                for x in opts:
                        if (x).startswith(text) or len(line.split())==1:
                                out.append(x)
                return out
        else:
                return opts


    def do_list_modules(self, line):
        """List all loaded modules with short description and supported devices.

    Usage: Just type list_modules without arguments to see what was loaded. """
        print "Loaded modules: "
        for m in self.modules:
                print "  - %s: %s [%s] " % (self.colorize(self.modules[m].name,"blue"), self.modules[m].short_description, ",".join([ str(x) for x in self.modules[m].get_available_devices()]))

    def do_list_devices(self, line):
        """List all loaded devices with short description and modules able to use them.

    Usage: Just type list_devices without arguments to see what was loaded. """
        print "Loaded devices: "
        for d in action_manager.get_all_devices_str():
                print "  - %s: %s [%s] " % (self.colorize(d,"blue"), 
                                            action_manager.device_map[d].short_description, 
                                            ",".join([ str(x) for x in action_manager.filter_supported_modules(action_manager.device_map[d], self.modules)])
                                           )

    def do_list_payloads(self, line):
        """List all loaded payloads with short description and modules able to use them.

    Usage: Just type list_payloads without arguments to see what was loaded. """
        print "Loaded payloads: "
        for p in self.payloads:
                print "  - %s: %s [%s] " % (self.colorize(p,"blue"), 
                                            self.payloads[p].short_description, 
                                            ",".join([ str(x) for x in action_manager.filter_supported_modules(self.payloads[p], self.modules)])
                                           )

    def do_list_actions(self, line):
        """List all loaded actions with short description and devices supporting them.

    Usage: Just type list_actions without arguments to see what was loaded. """
        print "Loaded actions: "
        for a in action_manager.actions:
                print "  - %s: %s [%s] " % (self.colorize(a,"blue"), 
                                            action_manager.actions[a].short_description, 
                                            ",".join([ str(x) for x in action_manager.actions_map[a]] if a in action_manager.actions_map else [])
                                           )

    def preloop(self):
        various.HID_singleton = self
        self.doc_header = "\n[ "+various.colorize("red","General commands")+" ]\n"

        for module in os.listdir(os.path.dirname(os.path.abspath(__file__))+"/"+consts.modules_dir):
                if module == '__init__.py' or module[-3:] != '.py':
                        continue
                try:
                        mod = __import__(consts.modules_dir+"."+module[:-3], locals(), globals(),module[:-3])
                        m = mod.init()
                        self.modules[m.name] = m
                except:
                        print self.colorize("!)","red")+" Error loading '%s' module ! " % module
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60
                        time.sleep(1)
        for device in os.listdir(os.path.dirname(os.path.abspath(__file__))+"/"+consts.devices_dir):
                if device == '__init__.py' or device[-3:] != '.py':
                        continue
                try:
                        dev = __import__(consts.devices_dir+"."+device[:-3], locals(), globals(),device[:-3])
                        dev = dev.init()
                        mesg = dev.dependency_check()
                        if mesg != "":
                                raise Exception(mesg)
                        mesg = action_manager.register_device(dev)
                        if mesg != "":
                                raise Exception(mesg)
                except Exception as e:
                        print self.colorize("!)","red")+" Error loading '%s' device ! " % device
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60
                        time.sleep(1)
        for payload in os.listdir(os.path.dirname(os.path.abspath(__file__))+"/"+consts.payloads_dir):
                if payload == '__init__.py' or payload[-3:] != '.py':
                        continue
                try:
                        pay = __import__(consts.payloads_dir+"."+payload[:-3], locals(), globals(),payload[:-3])
                        p = pay.init()
                        self.payloads[p.name] = p
                except:
                        print self.colorize("!)","red")+" Error loading '%s' payload ! " % payload
                        print '-'*60
                        traceback.print_exc(file=sys.stdout)
                        print '-'*60
                        time.sleep(1)

if __name__ == '__main__':
    app = HID()
    app.cmdloop()

