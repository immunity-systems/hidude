import re
import sys 

HID_singleton = None

def print_warning(text):
    print HID_singleton.colorize("!) ","red") + text

def print_info(text):
    print HID_singleton.colorize("OK) ","green") + text

def print_color(color,text):
    print HID_singleton.colorize(text,color)

def colorize(color,text):
    return HID_singleton.colorize(text,color)

def bold(txt):
    return "\033[1m" + txt + "\033[0;0m"

def strip_escape(txt):
    return re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', txt)

def payload_arg_unquote(s):
    return ((s[1:])[:-1]).replace("\\\\","\\").replace('\\"','"').replace("\\'","'")

def payload_arg_is_string(s):
    return s[0]=='"' or s[0]=="'"

spinner_text = ""
spinner_counter = 0
color = ['red', 'blue', 'green', 'cyan', 'magenta']

def spin_spinner():
    global spinner_counter
    global spinner_text
    global color 

    if len(spinner_text)<=spinner_counter:
        spinner_counter = 0
    sys.stdout.write("\033[K")
    sys.stdout.write("\033[F")
    print colorize("green","== ")+\
          spinner_text[0:spinner_counter]+\
          colorize(color[spinner_counter%len(color)],spinner_text[spinner_counter].upper())+\
          spinner_text[spinner_counter+1:]+\
          colorize("green"," ==")
    spinner_counter = spinner_counter + 1

def init_spinner(txt):
    global spinner_counter
    global spinner_text
    spinner_text = txt
    spinner_counter = 0
    #for new line
    print ""
    spin_spinner()

progress_text = ""

def progress(percent):
    global progress_counter
    global progress_text
    global color 

    sys.stdout.write("\033[K")
    sys.stdout.write("\033[F")
    prog = int((float(percent)/100) * 20)
    print progress_text+" "+\
          colorize("blue","[")+\
          colorize("green","#" * prog )+\
          (colorize("green","#" ) if percent == 100 else ">")+\
          colorize("red","_" * (19-prog))+\
          colorize("blue","]")+\
          " %.2f %%" % percent

def init_progress(txt):
    global progress_counter
    global progress_text
    progress_text = txt
    progress_counter = 0
    #for new line
    print ""
    progress(0)

