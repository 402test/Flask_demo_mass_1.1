import random

def get_active_code():
    randomStr = ""
    for i in range(18):
        temp = random.randrange(0, 3)
        if temp == 0:
            ch = chr(random.randrange(ord('A'), ord('Z') + 1))
            randomStr += ch
        elif temp == 1:
            ch = chr(random.randrange(ord('a'), ord('z') + 1))
            randomStr += ch
        else:
            ch = str((random.randrange(0, 10)))
            randomStr += ch
    return randomStr