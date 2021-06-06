import sys
import os
import uuid
import pprint
from datetime import date

current_date = date.today()
cwd = os.getcwd()
header_ID = "PACKAGE ID"
header_name = "FULL NAME"
header_description = "ITEM DESCRIPTION"
header_danger = "HAZARDOUS"
header_weight ="WEIGHT(kg)"
header_volume = "VOLUME(m^3)"
header_delivery = "DELIVERY DATE"
header_transport = "TRANSPORT"
header_cost = "COST($)"
dic_of_booking = {}
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
prompt = "*" * 160
prompt += "\n WELCOME TO BOOKING QUOTE SYSTEM"
prompt += "\n Press 1: 'Capture data'"
prompt += "\n Press 2: 'Display history of Bookings and Write CSV report'"
prompt += "\n Press 3: 'Exit program'"
prompt += "\n Type '1','2','3', then hit Enter: "


class Person:
    def __init__(self, first_name, last_name):
        self.last_name = last_name
        self.first_name = first_name

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Item:
    def __init__(self, description, hazard, weight, volume):
        self.description = description
        self.hazard = hazard # Yes or no
        self.weight = str(round(weight,2)) # Kg
        self.volume = str(round(volume,2)) # m^3
        self.weight_float = round(weight,2) # Kg
        self.volume_float = round(volume,2) # m^3


class Transport:
    def __init__(self, delivery_date, hazard, weight, volume):
        self.delivery_date = delivery_date
        self.delta_days = (delivery_date - current_date).days
        self.cost_air = max( 10*weight, 20*volume)
        self.hazard = hazard
        self.weight = weight
        self.volume = volume

    def transp(self):
        if self.hazard == "yes" or self.weight > 10 or self.volume > 125:
            return "land or sea"
        elif self.hazard == "no" and self.delta_days <= 3 and self.delta_days >= 0:
            return "air"
        elif self.hazard == "no" and self.delta_days > 3:
            return "air land or sea"
        else:
            return "n/a"


class Cost:
    def __init__(self, transport, cost_air, delta_days):
        self.transport = transport
        self.cost_air = cost_air
        self.delta_days = delta_days

        if self.transport == "air": # Urgent by air
            self.cost = str(self.cost_air)
        elif self.transport == "land or sea" and self.delta_days <= 3 and self.delta_days >= 0: # Urgent not air
            self.cost = str(45)
        elif self.transport == "land or sea" and self.delta_days > 3: # Not urgent, truck is cheaper
            self.cost = str(25)
        elif self.transport == "air land or sea":
            self.cost = str(min(self.cost_air, 25))
        elif self.transport == "n/a":
            self.cost ="n/a"
        else:
            self.cost = "not available"


# Get data
def capture_data():
    msg_first_name = clean_first_name() # Capitalized and not weird chars
    msg_last_name = clean_last_name() # Capitalized and not weird chars
    msg_description = clean_description() # Not weird chars
    msg_hazard = clean_hazard() # Yes or No
    msg_weight = clean_weight() # Float (kg)
    msg_volume = clean_volume() # Volume (m^3)
    msg_delivery_date = clean_delivery_date() # Date
    id = str(uuid.uuid4())
    # Instances #
    client = Person(msg_first_name,msg_last_name)
    item = Item(msg_description,msg_hazard,msg_weight,msg_volume)
    transport = Transport(msg_delivery_date,item.hazard,item.weight_float,item.volume_float)
    cost = Cost(transport.transp(),transport.cost_air,transport.delta_days)
    # tuple
    data_tuple=[
    client.full_name(),
    item.description,
    item.hazard,
    item.weight,
    item.volume,
    str(msg_delivery_date),
    transport.transp(),
    cost.cost
    ]
    dic_of_booking[id]=data_tuple
    write_csv()
    return dic_of_booking

def write_csv():
    try:
        with open(cwd + "\\" + "booking_records.csv", "w") as file:
            content = "PACKAGE ID,FULL NAME,ITEM DESCRIPTION,HAZARDOUS,WEIGHT(kg),VOLUME(m^3),DELIVERY DATE,TRANSPORT,COST($)\n"
            for k, v in dic_of_booking.items():
                content += k + ","
                for i in range(len(v)):
                    if i == (len(v) - 1):
                        content += v[i] + "\n"
                    else:
                        content += v[i] + ","
            file.write(content)
    except PermissionError:
        print("**Close csv file while using the System!**")
        print("**WARNING, Record not saved!**")


def display_bookings():
    print('\n')
    print("{:^40}{:^20}{:^20}{:^10}{:^11}{:^14}{:^14}{:^20}{:^10}".format(
    header_ID,
    header_name,
    header_description,
    header_danger,
    header_weight,
    header_volume,
    header_delivery,
    header_transport,
    header_cost
    )
    )
    # Check zip function
    for k, v in dic_of_booking.items():
        name, description, danger, weight, volume, delivery, transp, cost = v
        print ("{:^40}{:^20}{:^20}{:^10}{:^11}{:^14}{:^14}{:^20}{:^10}".format(
        k,name,description,danger,weight,volume,delivery,transp,cost
        )
        )


def clean_first_name():
    first_name = input("\nType FIRST NAME: ")
    first_name = unwanted_chars_fun(first_name)
    first_name = first_name.strip()
    return first_name.capitalize()


def clean_last_name():
    last_name = input("\nType LAST NAME: ")
    last_name = unwanted_chars_fun(last_name)
    last_name = last_name.strip()
    return last_name.capitalize()


def clean_description():
    msg_description = input("\nType PACKAGE DESCRIPTION: ")
    msg_description = unwanted_chars_fun(msg_description)
    return msg_description


def clean_hazard():
    yes_no = {
    "yes": "y",
    "no": "n",
    }
    while True:  # Validate yes or no
        msg_hazard = input("\nDoes package contain HAZARDOUS MATERIALS? (yes/no): ")
        try:
            yes_no[msg_hazard.lower()]
            break
        except KeyError:
            print("\nplease type only 'yes' or 'no' ")
        continue
    return msg_hazard.lower()


def clean_weight():
    while True:  # Validate yes or no
        msg_weight = input("\nEnter PACKAGE WEIGHT in kilograms: ")
        try:
            float(msg_weight)
            break
        except ValueError:
            print("\nplease type only numbers (Kg) ")
        continue
    return float(msg_weight)


def clean_volume():
    while True:  # Validate height
        msg_height = input("\nEnter PACKAGE HEIGHT in meters: ")
        try:
            float(msg_height)
            break
        except ValueError:
            print("\nplease type only numbers (m) ")
        continue
    while True:  # Validate length
        msg_length = input("\nEnter PACKAGE LENGTH in meters: ")
        try:
            float(msg_length)
            break
        except ValueError:
            print("\nplease type only numbers (m) ")
        continue
    while True:  # Validate width
        msg_width = input("\nEnter PACKAGE WIDTH in meters: ")
        try:
            float(msg_width)
            break
        except ValueError:
            print("\nplease type only numbers (m) ")
        continue
    volume_tuple = ( float(msg_height), float(msg_length), float(msg_width) )
    volume = float(msg_height)*float(msg_length)*float(msg_width)
    return volume # (m^3)


def clean_delivery_date():
    while True:  # Validate height
        msg_year = input("\nEnter YEAR DELIVERY DATE, (YYYY) format: ")
        msg_month = input("\nEnter MONTH DELIVERY DATE, (mm) format: ")
        msg_day = input("\nEnter DAY DELIVERY DATE, (dd) format: ")
        try:
            delivery_date = date(int(msg_year),int(msg_month),int(msg_day))
            break
        except SyntaxError:
            print("\nplease no leading zeros in dates ")
        except ValueError:
            print("\nplease enter a valid date (no leading zeros)")
        except NameError:
            print("\nplease enter only numbers (no leading zeros)")
        except TypeError:
            print("\nplease enter only numbers (no leading zeros)")
        continue
    return delivery_date


def unwanted_chars_fun(text):
    for i in unwanted_chars:
        text = text.replace(i, "")
    return text


def salir():
    sys.exit()

# TO DO AUTOMATED TESTS #
def main():
    main_d = {
        "1": capture_data,
        "2": display_bookings,
        "3": salir,
    }
    while True:
        try:
            main_d[input(prompt)]()
        except KeyError:
            print("Not a valid option!")

if __name__ == "__main__":
    main()
