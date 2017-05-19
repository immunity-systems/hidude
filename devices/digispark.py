__author__ = "Karol Celinski"
__copyright__ = "Copyright 2017, Immunity Systems Sp. z o.o."
__credits__ = ["Andrzej Nowodworski", "Pawel Maziarz"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Karol Celinski"
__email__ = "karolc@immunity-systems.com"

from core.device import Device
import time
from core.various import *
from core.validators import *
import os
from core.action_manager import action_manager
import struct

class Digispark(Device):
    name = "Digispark"
    short_description = "AVR Attiny85 uC based cheap device with software USB support."
    info = """
    The Digispark is an Attiny85 based microcontroller development board 
    similar to the Arduino line, only cheaper, smaller, and a bit less 
    powerful. With a whole host of shields to extend its functionality 
    and the action to use the familiar Arduino IDE the Digispark is a 
    great way to jump into electronics, or perfect for when an Arduino 
    is too big or too much.

    Photo: %s
    """ % (os.path.dirname(__file__).strip()+"/digispark/photo.jpg").strip()
    dev_info = None
    dev = None
    parameters = {
                'digispark_print_dev_info': {
                        'description':"If true, device information will be printed when programing.",
                        'default':"True",
                        'required':"True",
                        'value':"True"
                },
                'digispark_repeat': {
                        'description':"If true, device will repeat programmed payload until end of world!.",
                        'default':"True",
                        'required':"True",
                        'value':"True"
                },
                'digispark_sleep_before_start': {
                        'description':"If true, device will sleep fixed miliseconds before start payload. See digispark_sleep_miliseconds.",
                        'default':"True",
                        'required':"True",
                        'value':"True"
                },
                'digispark_sleep_miliseconds': {
                        'description':"If digispark_sleep_before_start is true, device will sleep miliseconds fixed in this parameter.",
                        'default':"5000",
                        'required':"True",
                        'value':"5000"
                },
        }

    def validate(self):
        if not is_bool(self.parameters['digispark_print_dev_info']['value']):
            return "Invalid value of digispark_print_dev_info - should be True or False"
        if not is_bool(self.parameters['digispark_repeat']['value']):
            return "Invalid value of digispark_repeat - should be True or False"
        if not is_bool(self.parameters['digispark_sleep_before_start']['value']):
            return "Invalid value of digispark_sleep_before_start - should be True or False"
        if not is_number(self.parameters['digispark_sleep_miliseconds']['value'],True):
            return "Invalid value of digispark_sleep_miliseconds - should be positive number!"
        return ""

    def connect_digispark(self, usb):
        start = time.time()
        dev = None
        init_spinner("Now please insert digispark into USB port.")
        while start+30>time.time():
            dev = usb.core.find(idVendor=0x16d0, idProduct=0x0753)
            if dev is None:
                spin_spinner()
                time.sleep(0.3)
                continue
            else:
                break
        return dev

    def program_erase(self, usb, dev):
          r = dev.ctrl_transfer(
                            usb.util.ENDPOINT_OUT|usb.util.CTRL_TYPE_VENDOR|usb.util.CTRL_RECIPIENT_DEVICE, 
                            2, 
                            0, 
                            0, 
                            None,
                            0xffff
                          )
          i = 0
          init_spinner("Erasing Digispark...")
          while (i < 100):
            spin_spinner()
            time.sleep(float(self.dev_info['erase_sleep']) / 1000 / 100);
            i = i + 1
          return r

    def program_write_flash(self, program, program_size, dev, usb):
         init_progress("Programming")
         page_length = self.dev_info['page_size'];
         page_buffer = []  # size of page_length
         address = None  # overall flash memory address
         page_address = None  # address within this page when copying buffer
         res = 0  # helper
         pagecontainsdata = False
         userReset = None
 
         address = 0
         #for (address = 0; address < deviceHandle->flash_size; address += deviceHandle->page_size) {
         while address < self.dev_info['flash_size']:
            progress((float(address)/self.dev_info['flash_size'])*100)
            # work around a bug in older bootloader versions
            if (
                    self.dev_info['major'] == 1 and
                    self.dev_info['minor'] <= 2 and
                    address / self.dev_info['page_size'] == self.dev_info['pages'] - 1
            ):
                    page_length = self.dev_info['flash_size'] % self.dev_info['page_size']
            pagecontainsdata = False
            #copy in bytes from user program
            page_buffer = [0] * page_length
            for page_address in range(page_length):
                if (address + page_address > program_size):
                    # pad out remainder with unprogrammed bytes
                    page_buffer[page_address] = 0xff
                else:
                    pagecontainsdata = True  # page contains data and needs to be written
                    page_buffer[page_address] = program[address + page_address];  # load from user program
            #Reset vector patching is done in the host tool in micronucleus >=2
            if (self.dev_info['major'] >= 2):
                if (address == 0):
                    # save user reset vector (bootloader will patch with its
                    # vector)
                    word0 = page_buffer[1] * 0x100 + page_buffer[0]
                    word1 = page_buffer[3] * 0x100 + page_buffer[2]
                    if (word0 == 0x940c):  # long jump
                        userReset = word1
                    elif ((word0 & 0xf000) == 0xc000):  # rjmp
                        userReset = (word0 & 0x0fff) - 0 + 1
                    else:
                        return "The reset vector of the user program does not contain a branch instruction,\n" +\
                               "therefore the bootloader can not be inserted. Please rearrage your code.\n"
                    # Patch in jmp to bootloader.
                    if (self.dev_info['bootloader_start'] > 0x2000):
                        #jmp
                        data = 0x940c;
                        page_buffer[0] = data >> 0 & 0xff
                        page_buffer[1] = data >> 8 & 0xff
                        page_buffer[2] = self.dev_info['bootloader_start'] >> 0 & 0xff
                        page_buffer[3] = self.dev_info['bootloader_start'] >> 8 & 0xff
                    else:
                        # rjmp
                        data = 0xc000 | ( (self.dev_info['bootloader_start'] / 2 - 1) & 0x0fff)
                        page_buffer[0] = data >> 0 & 0xff
                        page_buffer[1] = data >> 8 & 0xff
                #// if (address == 0 ):
                if (address >= self.dev_info['bootloader_start'] - self.dev_info['page_size']):
                    #move user reset vector to end of last page
                    #The reset vector is always the last vector in the tinyvectortable
                    user_reset_addr = (self.dev_info['pages'] * self.dev_info['page_size']) - 4
                    if (user_reset_addr > 0x2000):
                        #  jmp
                        data = 0x940c
                        page_buffer[user_reset_addr - address + 0] = data >> 0 & 0xff
                        page_buffer[user_reset_addr - address + 1] = data >> 8 & 0xff
                        page_buffer[user_reset_addr - address + 2] = userReset >> 0 & 0xff
                        page_buffer[user_reset_addr - address + 3] = userReset >> 8 & 0xff        
                    else:
                        # rjmp
                        data =  0xc000 | ((userReset - user_reset_addr/2 - 1) & 0x0fff)
                        page_buffer[user_reset_addr - address + 0] = data >> 0 & 0xff
                        page_buffer[user_reset_addr - address + 1] = data >> 8 & 0xff
            #// if ( self.dev_info['major'] >=2 ):
            #always write last page so bootloader can insert the tiny vector table
            if ( address >= self.dev_info['bootloader_start'] - self.dev_info['page_size'] ):
                  pagecontainsdata = True
            #ask microcontroller to write this page's data
            if pagecontainsdata:
                if (self.dev_info['major'] == 1):
                    #Firmware rev.1 transfers a page as a single block
                    #ask microcontroller to write this page's data
                    res = dev.ctrl_transfer(
                                    usb.util.ENDPOINT_OUT | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
                                    1,
                                    page_length, 
                                    address,
                                    ''.join([ x if type(x)==str else chr(x) for x in page_buffer[0:page_length] ] ), 
                                    0xffff
                          )
                elif (self.dev_info['major'] >= 2):
                    #Firmware rev.2 uses individual set up packets to transfer data
                    res = dev.ctrl_transfer(
                                   usb.util.ENDPOINT_OUT | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
                                   1, 
                                   page_length, 
                                   address, 
                                   None, 
                                   0xffff
                          )
                    if res!=0:
                        return "Error programming Digispark !"
                    #for (i=0; i< page_length; i+=4)
                    for i in range(0,page_length,4):
                        w1=(page_buffer[i+1]<<8)+(page_buffer[i+0]<<0)
                        w2=(page_buffer[i+3]<<8)+(page_buffer[i+2]<<0)
                        res = dev.ctrl_transfer(
                                    usb.util.ENDPOINT_OUT | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE,
                                    3, 
                                    w1, 
                                    w2, 
                                    None, 
                                    0xffff
                        )
                        if res!=0:
                            return "Error programming Digispark !"
                #give microcontroller enough time to write this page and come back online
                time.sleep(float(self.dev_info['write_sleep'])/1000)
            # // if pagecontainsdata:
            address = address + self.dev_info['page_size']
         #while address < self.dev_info['flash_size']:
         progress(100)
         return ""

    def get_info(self, usb, dev):
        minor = dev.bcdDevice & 0xFF;
        major = (dev.bcdDevice >> 8) & 0xFF;
        dev.set_configuration()
        info  = dev.ctrl_transfer(usb.util.ENDPOINT_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE, 0, 0, 0, 4)
        buf = info
        flash_size = ( (buf[0]<<8) + buf[1])
        page_size = buf[2]
        pages = flash_size / page_size
        if (pages * page_size < flash_size):
                pages = pages + 1
        bootloader_start = pages*page_size
        write_sleep = (buf[3] & 127)
        erase_sleep = write_sleep * pages
        self.dev_info =  {
            "major":major,
            "minor":minor,
            "flash_size":flash_size,
            "page_size":page_size,
            "pages":pages,
            "bootloader_start":bootloader_start,
            "write_sleep":write_sleep,
            "erase_sleep":write_sleep*pages
        }

    def print_info(self):
        print_info(
            "Detected Digispark info\n"+\
            "==============================\n"
            "Firmware version %i.%i\n" % (self.dev_info["major"],self.dev_info["minor"])+\
            "flash_size = %iB\n" % self.dev_info["flash_size"]+\
            "page_size = %iB\n" % self.dev_info["page_size"]+\
            "pages = %i" % self.dev_info["pages"]+\
            "bootloader_start = %i\n" % self.dev_info["bootloader_start"]+\
            "write sleep = %ims\n" % self.dev_info["write_sleep"]+\
            "erase_sleep = %ims\n" % self.dev_info["erase_sleep"]+\
            "==============================\n"
        )

    def action_program(self, input):
        import usb.core
        import usb.util
        import intelhex
        self.dev_info = None
        success = False
        dev = self.connect_digispark(usb)
        if dev != None:
            print_info("Digispark detected!")
            self.get_info(usb, dev)
            if self.parameters["digispark_print_dev_info"]["value"].upper()=="TRUE":
                self.print_info()
            if self.program_erase(usb, dev) !=0:
                return "Error erasing deigispark!"
            firmware = [0xff] * (65536 + 256)
            ih = intelhex.IntelHex()
            ih.loadhex((os.path.dirname(__file__).strip()+"/digispark/digispark_keyboard_firmware.hex").strip())
            f_size = 0
            for k,v in ih.todict().iteritems():
                firmware[int(k)] = chr(v)
                f_size = int(k) if int(k)>f_size else f_size
            stat,firmware = self.patch_firmware(firmware, input)
            if stat != "":
                return "Error patching firmware: %s " % stat
            self.program_write_flash(firmware, f_size, dev, usb)
            return ""
        else:
            return "Digispark not detected in 30s aborting!"

    def action_keyboard_write(self, input):
        return [ { "type" : "keyboard_write", "input": input } ]
 
    def action_mouse_move(self, input):
        return [ { "type" : "mouse_move", "move":input} ]

    def action_mouse_click(self, input):
        return [ { "type" : "mouse_click", "buttons":input} ]
 
    def action_mouse_scroll(self, input):
        return [ { "type" : "mouse_scroll", "scroll":input} ]

    def action_sleep(self, input):
        return [ { "type" : "sleep", "time":input} ]

    def dependency_check(self):
        try:
            import usb.core
            import usb.util
            import intelhex
        except Exception as e:
            return str(e)
        return ""
    
    def patch_firmware(self, firmware, payload):
        str_f = ''.join([ chr(x) if type(x)!=str else x for x in firmware ])
        begin = str_f.find("PAYLOAD")
        end   = str_f.rfind("PAYLOAD") + 7
        max_payload_size = end - begin
        print_info("Max payload size: %i" % max_payload_size)
        written = 0
        out_firm = firmware
        for command in payload:
           raw=""
           if command['type'] == "keyboard_write":
                raw = action_manager.actions["keyboard_write"].translate(command['input'])
           elif command['type'] == "sleep":
                raw = [x for x in "\x8e"+ struct.pack('i',int(command['time'][0]))]
           elif command['type'] == "mouse_click":
                raw = [x for x in "\x8f"+ struct.pack('b',int(command['buttons'][0]))]
           elif command['type'] == "mouse_move":
                raw = [x for x in "\x90"+ struct.pack('bb',int(command['move'][0]), int(command['move'][1]))]
           elif command['type'] == "mouse_scroll":
                raw = [x for x in "\x91"+ struct.pack('b',int(command['scroll'][0]))]
           else:
                return ("Unknown action occured during firmware patch !", None)
           #combo support
           raw_temp = []
           for x in raw:
               if type(x)==list:
                    if(len(x)>3):
                        return ("More than 3 characters simultaneously not supported on digispark!", None)
                    raw_temp.append(0xf0 + len(x))
                    raw_temp = raw_temp + x
               else:
                    raw_temp.append(x)
                
           raw = raw_temp
           out_firm = out_firm[0:begin+written] + raw + out_firm[begin+written+len(raw):]
           written = written + len(raw)
           if written>max_payload_size:
               return ("Payload too big!",None)
        out_firm[begin+written]=0
        written=written+1
        #config
        cnf_loc = str_f.find("CONFXX")
        if cnf_loc == -1:
            return ("Fatal error - no configuration section found in firmware!", None)
        """
         ABDDDD
         A - Repeat payload - 0 or 1
         B - Sleep before start - 0 or 1
         D - number of miliseconds to sleep
        """
        out_firm = out_firm[0:cnf_loc] +\
                   ["\x01" if self.parameters['digispark_repeat']['value'].upper()=="TRUE" else "\x00"] +\
                   ["\x01" if self.parameters['digispark_sleep_before_start']['value'].upper()=="TRUE" else "\x00"] +\
                   [x for x in struct.pack('i',int(self.parameters['digispark_sleep_miliseconds']['value']))]+\
                   out_firm[cnf_loc+6:]
        print_info("Payload size: %i ( %.2f %% ) " % ( written, (float(written)/max_payload_size )*100) ) 
        return ("", out_firm)



def init():
    return Digispark()