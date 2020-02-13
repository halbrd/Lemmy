from random import randint
 
def randomLenny():
    ears = ["( )", "[ ]", "{ }", "| |", "q p"]
    outsidearms = ["ᕙ ᕗ", "ヽ ﾉ", "\\ /", "乁 ㄏ", "└ ┘"]
    insidearms = ["☞ ☞", "づ づ", "ง ง"]
    eyes = ["͡° ͡°", "͠° °", "´• •`", "> <", "⚆ ⚆", "ᵔ ᵔ", "> >", "T T", "^ ^", "◕ ◕", "♥ ♥", "¬ ¬", "ಠ ಠ", "σ σ"]
    mouths = ["͜ʖ", "ᴥ", "ᗜ", "Ꮂ", "╭͜ʖ╮", "͟ʖ", "ω", "﹏", "‿", "╭╮", "益"]
 
    lenny = " "
    if randint(0, 3) == 0:
        if randint(0, 2) != 0:
            lenny = lenny.replace(" ", outsidearms[randint(0, len(outsidearms)-1)])
            lenny = lenny.replace(" ", ears[randint(0, len(ears)-1)])
        else:
            lenny = lenny.replace(" ", ears[randint(0, len(ears)-1)])
            ear = lenny[len(lenny)-1:len(lenny)]
            newlenny = lenny[:-1]
            newlenny = newlenny.replace(" ", insidearms[randint(0, len(insidearms)-1)])
            arm = newlenny[len(newlenny)-1:len(newlenny)]
            newlenny = newlenny[:-1]
            end = "".join((ear, arm))
            lenny = "".join((newlenny, end))
    else:
        lenny = lenny.replace(" ", ears[randint(0, len(ears)-1)])
    lenny = lenny.replace(" ", eyes[randint(0, len(eyes)-1)])
    lenny = lenny.replace(" ", mouths[randint(0, len(mouths)-1)])
    return(lenny)