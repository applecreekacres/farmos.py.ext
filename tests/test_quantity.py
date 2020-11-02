from farmer.ext.others import Measure
from farmer import Quantity
from farmer import Farm


def test_quantity():
    quantity = Quantity(Measure('weight'), 'Test', 'Pounds', '34')

    assert quantity.label == 'Test'
    assert quantity.measure == Measure.WEIGHT
    assert quantity.value == '34'
    assert quantity.unit == 'Pounds'
