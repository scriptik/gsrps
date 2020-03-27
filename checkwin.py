def gscheckWin(user, gameshell):
    win = False
    equal = False
    if (user == 0):
        if (gameshell == 2):
            win = True
            equal = False
        elif (gameshell == 1):
            win = False
            equal = False
        elif (gameshell == 0):
            equal = True

    elif (user == 1):
        if (gameshell == 0):
            win = True
            equal = False
        elif (gameshell == 2):
            win = False
            equal = False
        elif (gameshell == 1):
            equal = True

    else:
        if (gameshell == 1):
            win = True
            equal = False
        elif (gameshell == 0):
            win = False
            equal = False
        elif (gameshell == 2):
            equal = True

    if (equal == True):
        #return "equal"
        return 2
    elif (win):
        #return "Win"
        return 0
    else:
        #return "Lose"
        return 1
