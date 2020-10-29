"""Create a new Planting."""

from datetime import date, datetime, timedelta

import colorama

from farmer.ext.farm import Crop, CropFamily, Farm
from farmer.ext.output import alert, debug, info, init, message
from farmer.ext.prompt import prompt, prompt_date, prompt_number, prompt_yes_no


def main():
    """Script entry."""
    init('planting.log')
    print("Creating a new planting...")
    farm = Farm()
    season = determine_season(farm)
    crop = determine_crop(farm)
    seeding = schedule_seeding(farm)
    crop_info = get_crop_info(crop, farm)
    transplant = schedule_transplant(crop_info, seeding['date'], farm)
    harvest = schedule_harvest(transplant['date'], crop_info, seeding['date'])
    good = review_plan(crop, seeding, transplant, harvest)
    if good:
        location = transplant['location'] if transplant else seeding['location']
        planting = create_planting(farm, crop_info, season, location)
        create_seeding(farm, planting, seeding, crop_info)
        if transplant['date']:
            create_transplant(farm, planting, transplant)
        if harvest['date']:
            create_harvest(farm, planting, harvest)


def determine_season(farm: Farm):
    seasons = [x.name for x in farm.seasons]
    return prompt("Season:", completion=seasons)


def create_planting(farm: Farm, crop: Crop, season: str, location: str):
    planting = farm.create_planting(crop, season, location)
    message("Created Planting: {}".format(planting.name))
    return planting


def create_seeding(farm: Farm, planting, seeding, crop: Crop):
    area = [x for x in farm.areas if x.name == seeding['location']][0]
    seed_log = farm.create_seeding(planting,
                        area,
                        crop,
                        datetime.combine(seeding['date'], datetime.min.time()),
                        seeding['seeds'],
                        seeding['source'])
    message("Created Seeding: {}".format(seed_log.name))
    return seed_log


def create_transplant(farm, planting, transplant):
    area = [x for x in farm.areas if x.name == transplant['location']][0]
    trans_log = farm.create_transplant(planting,
                                  area,
                                  datetime.combine(transplant['date'], datetime.min.time()),
                                  done=transplant['done'])
    message("Created Transplanting: {}".format(trans_log.name))


def create_harvest(farm, planting, harvest):
    harvest_log = farm.create_harvest(planting,
                               datetime.combine(harvest['date'], datetime.min.time()),
                               None,
                               harvest['done'])
    message("Created Harvest: {}".format(harvest_log.name))


def review_plan(crop, seeding, transplant, harvest):
    alert("Review the following information before it is published.")
    msg_fmt = "{: <20}{: >20}"
    message(msg_fmt.format("Planting:", crop),
            color=colorama.Fore.GREEN)
    message(msg_fmt.format("Seeding Date:",
                           seeding['date'].strftime("%Y-%m-%d")))
    message(msg_fmt.format("Seeding Location:", seeding['location']))
    message(msg_fmt.format("Seeds Needed:", seeding['seeds']))
    message(msg_fmt.format("Seed Lot:", seeding['lot']))
    message(msg_fmt.format("Done:", str(seeding['done'])))
    if transplant['date']:
        message("Transplant:", color=colorama.Fore.GREEN)
        message(msg_fmt.format(
            "Date:", transplant['date'].strftime("%Y-%m-%d")))
        message(msg_fmt.format("Location:", transplant['location']))
        message(msg_fmt.format("Done:", str(transplant['done'])))
    if harvest['date']:
        message("Harvest", color=colorama.Fore.GREEN)
        message(msg_fmt.format(
            "Date:", harvest['date'].strftime("%Y-%m-%d")))
        message(msg_fmt.format("Done:", str(harvest['done'])))
    return prompt_yes_no("Publish Planting?")


def schedule_harvest(transplant_date: datetime, crop: Crop, seed_date: datetime):
    harvest_date = None
    done = None
    if prompt_yes_no("Create a harvest?"):
        if prompt_yes_no("Base harvest date on crop date of maturity?"):
            if transplant_date:
                harvest_date = get_harvest_date(crop, transplant_date)
            else:
                harvest_date = get_harvest_date(crop, seed_date)
            if not harvest_date:
                alert("Maturity data not found. Please provid date.")
                harvest_date = prompt_date("Harvest Date")
        else:
            harvest_date = prompt_date("Harvest Date")
        if harvest_date < datetime.now().date():
            alert("This date occurs in the past!")
            done = prompt_yes_no("Mark this log as Done?")
    return {
        "date": harvest_date,
        "done": done,
    }


def schedule_transplant(crop: Crop, seed_date: datetime, farm: Farm):
    done = False
    transplant = prompt_yes_no("Create a transplant?")
    transplant_date = None
    location = None
    if transplant:
        if prompt_yes_no("Base transplant date on provided crop data?"):
            transplant_date = get_transplant_date(crop, seed_date)
            if not transplant_date:
                alert("Transplant data not found, please provide date.")
                transplant_date = prompt_date("Transplant Date")
            if transplant_date < datetime.now().date():
                alert("This date occurs in the past!")
                done = prompt_yes_no("Mark this log as Done?")
            location = prompt("Transplant Location",
                              completion=get_locations(farm))
    return {
        "date": transplant_date,
        "location": location,
        "done": done
    }


def determine_crop(farm: Farm):
    families, fam_ids = get_crop_families(farm)
    crop_family = prompt("Crop Family", completion=[x.name for x in families])
    crop = prompt("Crop", completion=get_crops(farm, fam_ids, crop_family))
    return crop


def schedule_seeding(farm: Farm):
    done = False
    seed_date = prompt_date("Seed Date")
    if seed_date < datetime.now().date():
        alert("This date occurs in the past!")
        done = prompt_yes_no("Mark log as Done?")
    num_seeds = 0
    if prompt_yes_no("Need help calculating needed seeds?"):
        num_beds = prompt_number("Number of beds")
        num_rows = prompt_number("Number of rows/bed")
        foot_rows = prompt_number("Number of feet/row")
        inch_seeds = prompt_number("Inches between seeds")
        num_seeds = (num_rows * foot_rows * 12 * num_beds) / inch_seeds
        alert("{} seeds needed for planting.".format(num_seeds))
    else:
        num_seeds = prompt_number("Number of Seeds")
    seed_location = prompt("Seed Location", completion=get_locations(farm))
    seed_source = prompt("Seed Source")
    seed_lot = prompt("Seed Lot Number")
    return {
        "date": seed_date,
        "location": seed_location,
        "lot": seed_lot,
        "seeds": num_seeds,
        "source": seed_source,
        "done": done
    }


def get_crop_info(crop_name: str, farm: Farm) -> Crop:
    crops = farm.crops
    for crop in crops:
        if crop_name in crop.name:
            return crop
    return None


def get_transplant_date(crop: Crop, seed_date: datetime) -> datetime:
    if crop:
        trans = crop.transplant_days
        if not trans:
            return trans
        else:
            return seed_date + timedelta(days=int(trans))
    return None


def get_harvest_date(crop: Crop, base_date) -> datetime:
    mature = crop.maturity_days
    if mature:
        return base_date + timedelta(days=int(mature))
    else:
        return None


def get_locations(farm: Farm):
    return [x.name for x in farm.areas]


def get_crop_families(farm: Farm):
    families = farm.crop_families
    fam_ids = {fam.name: fam.tid for fam in families}
    info("Crop Families: {}".format([x.name for x in families]))
    info("Crop Family IDs: {}".format(fam_ids))
    return families, fam_ids


def get_crops(farm: Farm, fam_ids, crop_family):
    crops = farm.crops
    crop_names = [x.name[str(x.name).index(
        '-')+2:] for x in crops if 'crop_family' in x._ref_objs and x._ref_objs['crop_family']['id'] == fam_ids[crop_family]]
    return crop_names


if __name__ == "__main__":
    main()
