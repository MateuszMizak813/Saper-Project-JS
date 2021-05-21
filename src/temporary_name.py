
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
