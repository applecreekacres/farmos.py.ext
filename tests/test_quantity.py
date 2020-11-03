from farmer import Farm
from farmer.ext import Measure, Quantity


def test_quantity():
    quantity = Quantity(Measure('weight'), 'Test', 'Pounds', '34')

    assert quantity.label == 'Test'
    assert quantity.measure == Measure.WEIGHT
    assert quantity.value == '34'
    assert quantity.unit == 'Pounds'
