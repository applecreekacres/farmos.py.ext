
from ext.farm import Farm, Crop
from ext.output import alert, error, init


def main():
    init('crops.log')
    farm = Farm()
    for crop in farm.crops:
        if not crop.crop_family:
            alert("Crop {} does not have an assigned family.".format(crop.name))


if __name__ == "__main__":
    main()
