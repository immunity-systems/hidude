class Device:
    name = "abstract class"
    info = ""
    short_description = ""
    """
    Device parameters
    """
    parameters = {
            'param': {
                    'description':"Param description",
                    'default':"DEFAULT VALUE",
                    'required':"True",
                    'value':"DEFAULT VALUE"
            }
    }
    def dependency_check(self):
        """
        Check if device got all required library on this machine
        Return error message or empty string if all is ok.
        """
        pass

    def get_actions(self):
        """
        Return actions provided by device.
        """
        actions = []
        for m in dir(self):
            if m.startswith("action_"):
                actions.append(m.strip("action_"))
        return actions

    def perform_action(self,ability,input):
        """
        Execute action
        """
        if "action_"+ability not in dir(self):
            raise "Unknown action!"
        return getattr(self,"action_"+ability)(input)
    
    def info(self):
        """
        Return some information about device.
        """
        return info

    def validate(self):
        """
        Should validate all parameters. This method is called in execute.
        Return error message or empty string.
        """
        return ""

    def __str__(self):
        """
        Print name of device.
        """
        return self.name
    

    