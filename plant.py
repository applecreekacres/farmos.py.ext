"""Create a new Planting."""

import logging
from datetime import date, datetime, timedelta

from ext.prompt import prompt, prompt_date, prompt_number, prompt_yes_no
from ext.output import message, alert, debug, info
from farm import farm


def main():
    logging.basicConfig(filename='plant.log', filemode='w', level=logging.INFO,
                        format='%(name)s - %(levelname)s - %(message)s')
    print("Creating a new planting...")
    my_farm = farm()
    families, fam_ids = get_crop_families(my_farm)
    crop_family = prompt("Crop Family", completion=families)
    crop = prompt("Crop", completion=get_crops(my_farm, fam_ids, crop_family))
    seed_date = prompt_date("Seed Date")
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
    seed_location = prompt("Seed Location", get_locations(my_farm))
    transplant = prompt_yes_no("Create a transplant?")
    crop_info = get_crop_info(crop, my_farm)
    if transplant:
        if prompt_yes_no("Base transplant date on provided crop data?"):
            transplant_date = get_transplant_date(crop_info, seed_date)
            if not transplant_date:
                alert("Transplant data not found, please provide date.")
                transplant_date = prompt_date("Transplant Date")
    if prompt_yes_no("Create a harvest?"):
        if prompt_yes_no("Base harvest date on crop date of maturity?"):
            if transplant:
                harvest_date = get_harvest_date(crop_info, transplant_date)
            else:
                harvest_date = get_harvest_date(crop_info, seed_date)
            if not harvest_date:
                alert("Maturity data not found. Please provid date.")
                harvest_date = prompt_date("Harvest Date")
        else:
            harvest_date = prompt_date("Harvest Date")
    alert("Review the following information before it is published.")


def get_crop_info(crop_name, my_farm):
    crops = my_farm.term.get("farm_crops")
    for crop in crops['list']:
        if crop_name in crop['name']:
            return crop
    return None


def get_transplant_date(crop, seed_date):
    if crop:
        trans = crop['transplant_days']
        if not trans:
            return trans
        else:
            return seed_date + timedelta(days=int(trans))
    return None


def get_harvest_date(crop_info, base_date):
    mature = crop_info['maturity_days']
    if mature:
        return base_date + timedelta(days=int(mature))
    else:
        return None


def get_locations(my_farm):
    area_names = []
    areas = my_farm.area.get()
    for area in areas['list']:
        area_names.append(area['name'])
    return area_names


def get_crop_families(my_farm):
    crop_fams = my_farm.term.get("farm_crop_families")
    families = []
    fam_ids = {}
    for fam in crop_fams['list']:
        families.append(fam['name'])
        fam_ids[fam['name']] = fam['tid']
    info("Crop Families: {}".format(families))
    info("Crop Family IDs: {}".format(fam_ids))
    return families, fam_ids


def get_crops(my_farm, fam_ids, crop_family):
    crops = my_farm.term.get("farm_crops")
    crop_names = []
    for crop in crops['list']:
        if 'crop_family' in crop:
            if crop['crop_family']['id'] == fam_ids[crop_family]:
                name = crop['name'][str(crop['name']).index('-')+2:]
                crop_names.append(name)
    return crop_names


if __name__ == "__main__":
    main()
