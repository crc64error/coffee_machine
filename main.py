# TODO Prompt user for beverage choice
# TODO (o)ff to turn of the machine
# TODO (r) to print a report with current resources and money in the till
# TODO When a user places and order, confirm resources available
# TODO *Improve resource report by only presenting choices if there is enough of resources to produce it
# TODO Coin processing
# TODO Check transaction for enough to cover cost
# TODO *Instead of refunding the money allow the user to insert more money or request refund
# TODO Make the beverage
# TODO Move menu choices to menu.py
# TODO Create a recipe.py
# TODO Create a refill ingredients secret menu choice with logging using an ingredients.py
# DONE Create and Update lifetime counters for beverages served.
# Rest in Peace Queen Elizabeth the 2nd of England. May you find rest.

# import ast
from datetime import datetime
from os import system
import pickle
import json
from menu import MENU
from resources import resources
from coins import coins # Till quantities to provide change: Pennies, nickles, dimes, quarters, half-dollars, small-dollars


system('clear')
# print(MENU) # Dict in a Dict
# print(resources) # dict
# print(coins)

# Global Variables
beverage = {}
recipe = {}
price = float(0.00)
change = float(0.00)
beverages_served = 0
total_served_today = 0
expresso_served_today = 0
latte_served_today = 0
cappuccino_served_today = 0

# def create_a_json(total_served_today, expresso_served_today, latte_served_today, cappuccino_served_today):
#     beverages_served = {"total_served_lifetime": total_served_today, "expresso_served_lifetime": expresso_served_today, "latte_served_lifetime": latte_served_today, "cappuccino_served_lifetime": cappuccino_served_today }
    
#     json_dict = json.dumps(beverages_served)
#     f = open('reports/coffee_served.json', 'w')
#     f.write(json_dict)
#     f.close()

def get_beverages_served_lifetime():
    """ Get lifetime counts of beverages served

    Returns:
        dict: The count of all beverages served by this machine for life.
    """
    with open('reports/coffee_served.json') as json_file:
        beverages_served_dict = json.load(json_file)
    return beverages_served_dict

def update_beverages_served_lifetime(total_served_today, expresso_served_today, latte_served_today, cappuccino_served_today):
    """Update lifetime count of beverages served

    Args:
        total_served_today (int): int
        expresso_served_today (int): int
        latte_served_today (int): int
        cappuccino_served_today (int): int
    """
    beverages_served_lifetime = get_beverages_served_lifetime()
    print(beverages_served_lifetime)
    # This feels messy
    total_served_today = {"total_served_lifetime": (beverages_served_lifetime.get("total_served_lifetime") + total_served_today)}
    expresso_served_today = {"expresso_served_lifetime": (beverages_served_lifetime.get("expresso_served_lifetime") + expresso_served_today)}
    latte_served_today = {"latte_served_lifetime": (beverages_served_lifetime.get("latte_served_lifetime") + latte_served_today)}
    cappuccino_served_today = {"cappuccino_served_lifetime": (beverages_served_lifetime.get("cappuccino_served_lifetime") + cappuccino_served_today)}
    beverages_served_lifetime.update(total_served_today)
    beverages_served_lifetime.update(expresso_served_today)
    beverages_served_lifetime.update(latte_served_today)
    beverages_served_lifetime.update(cappuccino_served_today)
    # Write the file
    json_dict = json.dumps(beverages_served_lifetime)
    f = open('reports/coffee_served.json', 'w')
    f.write(json_dict)
    f.close()
  

# Menu Toggles Should be False on boot for initial setup
cleaning_prompt = True
have_an_expresso = False
have_a_late = False
have_a_cappuccino = False

# in_machine_resources
in_machine_resources = {
    "water": {"status": 0, "capacity": 3000},
    "milk": {"status": 0, "capacity": 2000},
    "coffee": {"status": 0, "capacity": 1000},
}

machine_report = { # Template of the machine report
    "used_resources": {
        "water": 0,
        "milk": 0,
        "coffee": 0
    },
    "remaining_resources": {
        "water": 0,
        "milk": 0,
        "coffee": 0
    },
    "sales": {
        "expresso": 0,
        "latte": 0,
        "cappuccino": 0
    },
    "coins_in_till": {
        "pennies": 0,
        "nickles": 0,
        "dimes": 0,
        "quarters": 0,
        "half-dollars": 0,
        "small-dollars": 0
    },
    "coins_in_deposit": {
        "pennies": 0,
        "nickles": 0,
        "dimes": 0,
        "quarters": 0,
        "half-dollars": 0,
        "small-dollars": 0
    }        
}
    
# report_file_name = "report_" + str(datetime.now()) + ".log"
# f = open("reports/" + report_file_name, "w")

# f.write(str(machine_report))

# f.close()

get_beverages_served_lifetime()
update_beverages_served_lifetime(total_served_today,expresso_served_today, latte_served_today, cappuccino_served_today)

def boot_machine():
    # Prompt for setup steps
    if bool(input("Clean Machine? ")) ==  True:
        cleaning_prompt = False
        # Report dumped resources by appending to report_variable
    else:
        cleaning_prompt = True
        have_an_expresso = False
        have_a_late = False
        have_a_cappuccino = False
        # Add used resources to report_variable
    
    if bool(input("Refill machine?")) == True:
        refill

def shutdown_machine():
    """Shutdown Process
    """
    # Complete shutdown steps including unload_machine()
    print("Shutdown Procedure")

def build_report():
    """report building
    """
    report_file_name = "report_" + datetime.now() + ".log"
    f = open(report_file_name, "w")
    f.write(machine_report)
    f.close()

def refill(in_machine_resources):
    """Refill all ingredients

    Args:
        in_machine_resources (dict): list of stock items, water, coffee, milk
    """

    print("refill")
    
    
def request_payment(beverage):
    # Get price from menu
    # Count input change
    # Display change
    # Dispense change from till
    # if till is low, illuminate "Exact Change only" and do not give change
    # Sort and add coins given to till
    print(beverage('price'))
    
def clean_machine(cleaning_prompt):
    # every 300 beverages, trigger the clean soon indicator.
    # If a refill is needed and cleaning is with in 30 beverages, recommend cleaning
    print(clean_machine)
    
def check_resources(beverage, recipe): # This should run at the end of every transaction
    # If an ingredient is not enough for a recipe, toggle (refill_light) and remove that beverage from menu
    # If that beverage can not be made 
    print("Check Resources")
        
    
def make_beverage(beverage, recipe, in_machine_resources):
    match beverage:
        case "e": # Expresso
            if have_an_expresso == True:
                return "e"
        case "l": # Latte
            if have_a_late == True:
                return "l"
        case "c": # Cappuccino
            if have_a_cappuccino == True:
                 return "c"
        case _: # No match
            return "Invalid Selection, please try again"

coffee_emoji = "☕️"




