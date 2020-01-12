
import colorama
import logging

colorama.init()


def _message(msg: str, color):
    print(color, end="")
    print(msg)
    print(colorama.Fore.RESET)


def message(msg: str):
    _message(msg, colorama.Fore.WHITE)
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