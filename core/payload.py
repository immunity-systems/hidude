class Payload:
    """
    Name of payload.
    """
    name = None
    """
    Description.
    """
    info = None
    """
    Shor description
    """
    short_description = None
    """
    Actions that are satisfied by payload.
    """
    satisfied_actions = []
    """
    Payload parameters
    """
    parameters = {
            'param': {
                    'description':"Param description",
                    'default':"DEFAULT VALUE",
                    'required':"True",
                    "value":"DEFAULT VALUE"
            }
    }

    def get_payload(self):
        return None

    def validate(self):
            """
            Should validate all parameters. This method is called before get_payload in execute.
            Return error message or empty string.
            """
            return ""

    """
    If return true, module will be executed. If not - only get_payload will be called.
    Usually should be True. False can be for example if you only want to just generate 
    payload but without executing.
    """
    def do_execute(self):
            return True

    def __str__(self):
        return self.name
    