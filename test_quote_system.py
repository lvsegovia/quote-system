import quote_system
from datetime import date
current_date = date.today()

unwanted_chars = [
    ".",
    ",",
    ":",
    "!",
    "?",
    "*",
    "$",
    "(",
    ")",
    "-",
    "'",
    '"',
    ";",
    "@",
    "[",
    "]",
    "+",
    "-",
    "#",
    "%",
    "^",
    "&",
    "=",
    "_",
    "`",
    "/",
    "|",
    "{",
    "}",
    "\\",  # Backslash has to be doubled
]


def test_unwanted_chars_fun():
    assert "This is a test" == quote_system.unwanted_chars_fun(".T_(h)#is, :!?$i[s]% a@ {t/e|s*t}\\")


def test_Person():
    test_person = quote_system.Person("leo","segovia")
    assert "leo" == test_person.first_name
    assert "segovia" == test_person.last_name
    assert "leo segovia" == test_person.full_name()


def test_Item():
    test_item = quote_system.Item("guitar", "no", 2.551, .0512)
    assert "guitar" == test_item.description
    assert "no" == test_item.hazard
    assert "2.55" == test_item.weight
    assert "0.05" == test_item.volume
    assert 2.55 == test_item.weight_float
    assert .05 == test_item.volume_float

# This tests are time dependent, please check comments
def test_Transport():
    # Valid until 2021/12/12
    test_delivery_date = date(2021,12,15)
    test_transport = quote_system.Transport(test_delivery_date,"yes",3.0,1.5)
    test_transport2 = quote_system.Transport(test_delivery_date,"no",3.5,1.5)
    assert "2021-12-15" == str(test_transport.delivery_date)
    assert date(2021,12,15) == test_transport.delivery_date
    assert "yes" == test_transport.hazard
    assert "no" == test_transport2.hazard
    assert 3.0 == test_transport.weight
    assert 1.5 == test_transport.volume
    assert 30 == test_transport.cost_air
    assert 3.5 == test_transport2.weight
    assert 1.5 == test_transport2.volume
    assert 35 == test_transport2.cost_air
    assert "land or sea" == test_transport.transp()
    assert "air land or sea" == test_transport2.transp()
    ###### Valid only on the date they were tested (2021/6/6) ######
    test_delivery_date3 = date(2021,6,8)
    test_transport3 = quote_system.Transport(test_delivery_date3,"no",3.5,1.5)
    assert "2021-06-08" == str(test_transport3.delivery_date)
    assert date(2021,6,8) == test_transport3.delivery_date
    assert 2 == test_transport3.delta_days
    assert 35 == test_transport3.cost_air
    assert "no" == test_transport3.hazard
    assert 3.5 == test_transport3.weight
    assert 1.5 == test_transport3.volume
    assert "air" == test_transport3.transp()
    test_delivery_date4 = date(2021,5,6)
    test_transport4 = quote_system.Transport(test_delivery_date4,"no",3.5,1.5)
    assert -31 == test_transport4.delta_days
    assert "n/a" == test_transport4.transp()
    #### End of tests that are valid only for (2021/6/6) ####


def test_Cost():
    test_cost = quote_system.Cost("air", 35, 3)
    assert "air" == test_cost.transport
    assert 35 == test_cost.cost_air
    assert 3 == test_cost.delta_days
    assert '35' == test_cost.cost
    test_cost2 = quote_system.Cost("land or sea", 35, 3)
    assert '45' == test_cost2.cost
    test_cost3 = quote_system.Cost("land or sea", 35, 4)
    assert '25' == test_cost3.cost
    test_cost4 = quote_system.Cost("air land or sea", 15, 4)
    assert '15' == test_cost4.cost
    test_cost5 = quote_system.Cost("n/a", 15, 4)
    assert 'n/a' == test_cost5.cost
