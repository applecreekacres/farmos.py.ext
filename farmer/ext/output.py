
import colorama
import logging

colorama.init()


def init(name: str):
    logging.basicConfig(filename=name, filemode='w', level=logging.INFO,
                        format='%(name)s - %(levelname)s - %(message)s')


def _message(msg: str, color):
    print(color, end="")
    print(msg)
    print(colorama.Fore.RESET, end="")


def message(msg: str, level=0, color=colorama.Fore.WHITE):
    _message("{}{}".format("\t" * level, msg), color)
    logging.info(msg)


def info(msg: str):
    logging.info(msg)


def alert(msg: str):
    _message(msg, colorama.Fore.YELLOW)
    logging.warn(msg)


def error(msg: str):
    _message(msg, colorama.Fore.RED)
    logging.error(msg)


def debug(msg: str):
    _message(msg, colorama.Fore.GREEN)
    logging.debug(msg)