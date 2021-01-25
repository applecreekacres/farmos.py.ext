
from farmer import Farm
from farmer.reporting import RstReporter


def main():
    farm = Farm()
    with RstReporter("Crop Catalog") as report:
        report.toctree(1)
        report.heading("Crops", 1)
        for crop in farm.crops:
            report.heading(crop.name, 2)
            # for image in crop.images:
                # report.image(image.download())
            # if crop.crop_family:
                # report.definition("Family", crop.crop_family.name)
            report.line(crop.description)


if __name__ == "__main__":
    main()
