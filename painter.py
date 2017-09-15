RED = '\033[0;31m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
CYAN = '\033[0;36m'
GRAY = '\033[0;37m'
GREY = GRAY
NORMAL = '\033[0m'
RED_INV = '\033[7;31m'


def paint(message, color):
    return color + str(message) + NORMAL

