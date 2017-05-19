def is_number(s,positive=False):
    try:
        int(s)
        return float(s)>=0 if positive else True
    except ValueError:
        return False

def is_bool(s):
    return s.upper() in ["TRUE", "FALSE"]