
from farmer import Farm
from farmer.ext.asset import Planting
from farmer.reporting import RstReporter

YEAR = "2019"


def main():
    farm = Farm()
    with RstReporter("{} Report".format(YEAR)) as report:
        report.toctree(1)
        report.heading("Plantings", 1)
        for planting in farm.plantings({'season': YEAR}):
            for crop in planting.crop:
                report.heading(crop.name, 2)
                if planting.flags:
                    set_flags = [flag for flag in planting.flags]
                    report.definition("Flags", str(set_flags))
                if planting.description:
                    report.line(planting.description['value'])

                report_seedings(farm, planting, report)
                report_transplants(farm, planting, report)

        report.heading("Compost", 1)


def report_transplants(farm: Farm, planting: Planting, report: RstReporter):
    logs = []
    notes = []
    for transplant in farm.transplants({"asset": planting.id}):
        date = transplant.timestamp.strftime("%m/%d/%Y")
        logs.append({
            'Done': "\u2713" if transplant.done else '',
            'Date': date,
            'Area': ', '.join([area.name for area in transplant.movement]),
            # "Notes": transplant.notes if transplant.notes else ""
        })
        if transplant.notes:
            notes.append("**{}** - {}".format(date, transplant.notes))
    if logs:
        report.heading('Transplants', 3)
        report.table(logs)
    if notes:
        report.lists(notes, False)


def report_seedings(farm: Farm, planting: Planting, report: RstReporter):
    logs = []
    notes = []
    for seeding in farm.seedings({"asset": planting.id}):
        date = seeding.timestamp.strftime("%m/%d/%Y")
        logs.append({
            'Done': "\u2713" if seeding.done else '',
            'Date': date,
            'Area': ', '.join([area.name for area in seeding.movement]),
            'Seeds': ", ".join(
                ["{} {}".format(quantity.value,
                                quantity.unit['name'] if quantity.unit else '') for quantity in seeding.quantity]),
            # "Notes": seeding.notes if seeding.notes else ""
        })
        if seeding.notes:
            notes.append("**{}** - {}".format(date, seeding.notes))
    if logs:
        report.heading('Seedings', 3)
        report.table(logs)
    if notes:
        report.lists(notes, False)


if __name__ == "__main__":
    main()
