def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def is_yolo_format(*args):
    if(len(args) != 5):
        return False
    else:
        if(args[0].isdigit() and is_float(args[1]) and is_float(args[2]) and is_float(args[3]) and is_float(args[4])):
            return True
        else:
            return False