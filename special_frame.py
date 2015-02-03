from random import randint


def special_frame():
    TK = str(randint(0, 9)) + str(randint(0, 9))
    TB = str(randint(0, 9)) + str(randint(0, 9))
    ST = str(0) + str(randint(0, 1))
    PH = str(0) + str(randint(1, 6))
    charframe = chr(int('43', 16)) + \
        chr(int('41', 16)) + \
        chr(int('4e', 16)) + \
        chr(int('00', 16)) + \
        chr(int('01', 16)) + \
        chr(int('04', 16)) + \
        chr(int(TK, 16)) + \
        chr(int(TB, 16)) + \
        chr(int(ST, 16)) + \
        chr(int(PH, 16))

    return charframe
