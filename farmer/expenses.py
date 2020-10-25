"""Report on Farm expenses."""

from .ext.farm import Farm
from .ext.output import alert, info


def main():
    farm = Farm()
    expenses = farm.expense_logs
    info(expenses)

if __name__ == "__main__":
    main()
