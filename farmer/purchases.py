"""Create Purchase Logs."""

from .ext.farm import Farm
from .ext.output import alert, message
from .ext.prompt import prompt, prompt_date, prompt_number


def main():
    farm = Farm()
    message("Lets create a purchase log.")
    date = prompt_date("Date of purchase")
    seller = prompt("Seller")
    invoice = prompt_number("Invoice")
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
            "total": quantity * float(unit_cost)
        })


if __name__ == "__main__":
    main()
