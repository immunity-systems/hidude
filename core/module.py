from action_manager import action_manager

class Module:
    name = None
    short_description = None
    description = None
    required_actions = [] 
    parameters = {
            'param': {
                    'description':"Param description",
                    'default':"DEFAULT VALUE",
                    'required':"True",
            }
    }

    payload_actions = []

    def get_available_devices(self):
        return action_manager.get_supported_devices(self.required_actions)


    def validate(self):
            """
            Should validate all parameters. This method is called in execute.
            Return error message or empty string.
            """
            return ""

    def execute(self, paylad, device):
            """
            It's executed after all parameters all set.
            If all ok return "" else return error string.
            """
            pass
    """
    If set to true, module require device to be set before executing.
    If false, module can be executed without devices set.
    """
    def require_device(self):
            return True

    def __str__(self):
            return self.name
