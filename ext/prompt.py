"""Wrapper around prompt toolkit."""

from datetime import date, datetime, timedelta
import logging
from prompt_toolkit import prompt as prmpt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.validation import ValidationError, Validator


class DateValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and not text.isdigit():
            i = 0

            # Get index of fist non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(message='This input contains non-numeric characters',
                                  cursor_position=i)
        if text and not len(text) == 8:
            i = 0

            # Get index of fist non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(message='This input is not 8 digits long.',
                                  cursor_position=i)


class NumberValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and not text.isdigit():
            i = 0

            # Get index of fist non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(message='This input contains non-numeric characters',
                                  cursor_position=i)


class YesNoValidator(Validator):
    def validate(self, document):
        text = document.text

        if text and text not in ["y", "Y", "n", "N"]:
            i = 0

            # Get index of fist non numeric character.
            # We want to move the cursor here.
            for i, c in enumerate(text):
                if not c.isdigit():
                    break

            raise ValidationError(message='Value not y or n',
                                  cursor_position=i)


def prompt(message, validator=None, completion=None):
    complete = WordCompleter(completion) if completion else None
    response = prmpt("{} >".format(message), validator=validator, completer=complete, search_ignore_case=True)
    logging.info("{}: {}".format(message, response))
    return response


def prompt_date(message):
    response = prompt("{} [DDMMYYYY]".format(
        message), validator=DateValidator())
    form_date = datetime.strptime(response, "%m%d%Y").date()
    return form_date


def prompt_number(message: str):
    num = int(prompt(message, validator=NumberValidator()))
    logging.info("{}: {}".format(message, num))
    return num


def prompt_yes_no(message: str):
    response = prompt(message, validator=YesNoValidator())
    return True if response in ['y', 'Y'] else False
