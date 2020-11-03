"""Create Purchase Logs."""

from datetime import datetime
from .ext.farm import Farm
from .ext.output import message
from .ext.prompt import prompt, prompt_date, prompt_number


def main():
    farm = Farm()
    message("Lets create a purchase log.")
    date = prompt_date("Date of purchase")
    seller = prompt("Seller")
    item = "test"
    items = []
    while item:
        name = prompt("Item Name")
        quantity = prompt_number("Quantity")
        unit_cost = prompt("Unit Cost")
        units = farm.units
        units = prompt("Units",  completion=[x.name for x in units])
        items.append({
            "name": name,
            "quantity": quantity,
            "unit_cost": unit_cost,
            "units": units,
            "total": quantity * float(unit_cost),
            'seller': seller,
            'timestamp': datetime.combine(date, datetime.min.time()).timestamp()
        })


if __name__ == "__main__":
    main()
