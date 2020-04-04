"""Report on Farm expenses."""

from ext.farm import Farm
from ext.output import info, alert


def main():
    farm = Farm()
    expenses = farm.expense_logs
    info(expenses)

if __name__ == "__main__":
    main()
