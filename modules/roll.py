import random


def roll_die(roll_min, roll_max):
    # print (str(roll_min) + str(roll_max))
    roll_min = int(roll_min)
    roll_max = int(roll_max)
    if roll_min <= 0 or roll_max <= 0 or roll_min > 9999999999 or roll_max > 9999999999 or roll_min > roll_max:
        return ("Arguments must not be less than 0 or greater than 9999999999 and the minimum roll can not be greater than the maximum roll.")
    else:
        random_roll = (random.randint(roll_min, roll_max))
        return (" rolled a "+str(random_roll)+".")
