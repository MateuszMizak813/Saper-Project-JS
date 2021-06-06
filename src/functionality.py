import random
import gui


class Error(Exception):
    """ Podstawa pod inne własne klasy wyjątków"""
    pass


class WrongTypeOfArguments(Error):
    """ Błąd zwracany w wypadku nie odpowiedniego typu argumentów """
    def __init__(self, argument_name, content):
        self.content = content
        self.argument_name = argument_name


class ArgumentNotInRange(Error):
    """ Błąd zwracany w wypadku gdy argument wykracza poza dozwolony przedział """
    def __init__(self, argument_name, value):
        self.value = value
        self.argument_name = argument_name


def check_settings(height, width, mines):
    """ Funkcja sprawdzająca poprawność ustawień wprowadzonych przez użytkownika """
    if not height.isdigit():
        raise WrongTypeOfArguments("wysokość", height)
    elif int(height) < 2 or int(height) > 15:
        raise ArgumentNotInRange("wysokość", height)

    if not width.isdigit():
        raise WrongTypeOfArguments("szerokość", width)
    elif int(width) < 2 or int(width) > 15:
        raise ArgumentNotInRange("szerokość", width)

    if not mines.isdigit():
        raise WrongTypeOfArguments("ilość min", mines)
    elif int(mines) < 0 or int(mines) > int(width)*int(height):
        raise ArgumentNotInRange("ilość min", mines)


def get_minefield(h, w, m):
    """ Funkcja służąca do losowania min na planszy """
    random_positions = random.sample(range(h*w), k=m)
    mine_field = [[True if j*h+i in random_positions else False for i in range(w)]for j in range(h)]
    return mine_field


def check_surroundings(row, column, mine_field):
    """ Funkcja zwracająca liczbę min w okół pola """
    near_field_list = [(j, i) for j in [column - 1, column, column + 1] if 0 <= j < len(mine_field[0])
                       for i in [row - 1, row, row + 1] if 0 <= i < len(mine_field)]

    mines_list = [isinstance(mine_field[i][j], gui.SaperGame.FieldWithMine) for j, i in near_field_list]
    return mines_list.count(True), near_field_list
