class Action:
    """
    Name of action.
    """
    name = None
    """
    Description.
    """
    info = None
    """
    Short description
    """
    short_description = None

    def validate(self, payload):
            """
            Should validate payload syntax and return error string or empty string.
            """
            return ""

    def __str__(self):
        return self.name
 