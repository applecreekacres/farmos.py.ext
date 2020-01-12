"""Create a new Planting."""

import logging
from datetime import date, datetime

from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.validation import ValidationError, Validator

from farm import farm


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


def main():
    logging.basicConfig(filename='plant.log', filemode='w', level=logging.INFO,
                        format='%(name)s - %(levelname)s - %(message)s')
    print("Creating a new planting...")
    my_farm = farm()
    families, fam_ids = get_crop_families(my_farm)
    crop_family = prompt_crop_family(families)
    crop = prompt_crop(my_farm, fam_ids, crop_family)
    seed_date = prompt_seed_date()
    num_seeds = 0
    if prompt_yes_no("Need help calculating needed seeds?"):
        num_beds = prompt_number("Number of beds")
        num_rows = prompt_number("Number of rows/bed")
        foot_rows = prompt_number("Number of feet/row")
        inch_seeds = prompt_number("Inches between seeds")
        num_seeds = (num_rows * foot_rows * 12 * num_beds) / inch_seeds
        logging.info("{} seeds needed for planting.".format(num_seeds))
    else:
        num_seeds = prompt_number("Number of Seeds")
    location = prompt_location(my_farm)


def prompt_location(my_farm):
    area_names = []
    areas = my_farm.area.get()
    for area in areas['list']:
        area_names.append(area['name'])
    area_completer = WordCompleter(area_names)
    location = prompt("Location of seeding >",
                      auto_suggest=AutoSuggestFromHistory(),
                      history=FileHistory("farm_area_history.txt"),
                      completer=area_completer)
    logging.info("Location: {}".format(location))
    return location


def prompt_number(message: str):
    num = int(prompt("{} >".format(message), validator=NumberValidator()))
    logging.info("{}: {}".format(message, num))
    return num


def prompt_yes_no(message: str):
    response = prompt("{} >".format(message), validator=YesNoValidator())
    return True if response in ['y', 'Y'] else False


def prompt_seed_date():
    seed_date = prompt("Seed Date [DDMMYYYY] >", validator=DateValidator())
    str_date = datetime.strptime(seed_date, "%m%d%Y").date()
    logging.info("Provided date {}".format(str_date))
    return str_date


def prompt_crop_family(families):
    crop_family = prompt("Crop Family >", completer=WordCompleter(families),
                         auto_suggest=AutoSuggestFromHistory(),
                         search_ignore_case=True,
                         history=FileHistory("crop_family_history.txt"))
    logging.info("Crop Family: {}".format(crop_family))
    return crop_family


def get_crop_families(my_farm):
    crop_fams = my_farm.term.get("farm_crop_families")
    families = []
    fam_ids = {}
    for fam in crop_fams['list']:
        families.append(fam['name'])
        fam_ids[fam['name']] = fam['tid']
    logging.info("Crop Families: {}".format(families))
    logging.info("Crop Family IDs: {}".format(fam_ids))
    return families, fam_ids


def prompt_crop(my_farm, fam_ids, crop_family):
    crops = my_farm.term.get("farm_crops")
    crop_names = []
    for crop in crops['list']:
        if 'crop_family' in crop:
            if crop['crop_family']['id'] == fam_ids[crop_family]:
                name = crop['name'][str(crop['name']).index('-')+2:]
                crop_names.append(name)
    crop_complete = WordCompleter(crop_names)
    crop = prompt("Crop >", completer=crop_complete, search_ignore_case=True,
                  auto_suggest=AutoSuggestFromHistory(),
                  history=FileHistory("crop_history.txt"))
    logging.info("Crop: {}".format(crop))
    return crop


if __name__ == "__main__":
    main()
