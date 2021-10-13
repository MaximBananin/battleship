import logging
from copy import deepcopy

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



def check_ship(x, y, size, direction, battlefield):
    ''' Successful check returns true. '''
    
    if check_collision(x, y, size, direction, battlefield):
        logger.info('Collision')
        return False

    elif check_contact(x, y, size, direction, battlefield):
        logger.info('Collision')
        return False

    elif check_posible(x, y, size, direction, battlefield):
        logger.info('Out of field')
        return False

    for i in range(size):
        if check_around(x, y, battlefield):
            logger.info('Around')
            return False
        if direction:
            x += 1
        else:
            y += 1
    return True


def check_around(x, y, battlefield):
    for place in ((x-1, y-1), (x-1, y+1), (x+1, y-1), (x+1, y+1)):
        if check_place(place[0], place[1], battlefield):
            print(f'Check place for {x}:{y}')
            return True
    return False


def check_collision(x, y, size, direction, battlefield):
    for i in range(size):
        if check_place(x, y, battlefield):
            return True

        if direction:
            x += 1
        else:
            y += 1
    return False


def check_posible(x, y, size, direction, battlefield):
    ''' Check out of field '''

    for i in range(size):
        try:
            check = battlefield[y][x]
        except IndexError:
            return True
        if direction:
            x += 1
        else:
            y += 1
    return False

def check_place(x, y, battlefield):
    ''' Returns True if there is a ship. '''
    try:
        if battlefield[y][x] in (1, 3):
            return True
        return False
    except IndexError:
        return False


def hidden_ships(battlefield):
    result = deepcopy(battlefield)
    for row_index, row in enumerate(result):
        for index, place in enumerate(row):
            if place == 1:
                result[row_index][index] = 0
    return result


def check_contact(x, y, size, direction, battlefield):
    ''' Monster function becose ships dont have class
        Take ship, returns collision with another ship
        about rear deck and bow'''

    result = []
    if direction:
        x -= 1
        try:
            result.append(check_place(x, y, battlefield))
        except IndexError:
            pass
        x = x + size + 2
        try:
            result.append(check_place(x, y, battlefield))
        except IndexError:
            pass
    else:
        y -= 1
        try:
            result.append(check_place(x, y, battlefield))
        except IndexError:
            pass
        y = y + size + 2
        try:
            result.append(check_place(x, y, battlefield))
        except IndexError:
            pass
    return any(result)
