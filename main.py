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
# Rest in Peace Queen Elizabeth the 2nd of England. May you find rest.

import ast
from datetime import datetime
from os import system
from menu import MENU
from resources import resources
from coins import coins # Till quantities to provide change: Pennies, nickles, dimes, quarters, half-dollars, small-dollars


system('clear')
print(MENU) # Dict in a Dict
print(resources) # dict
print(coins)

# Global Variables
beverage = {}
recipe = {}
price = float(0.00)
change = float(0.00)
beverages_served = 0

def get_beverages_served_lifetime():
    f = open('DAY_015/coffee_machine/reports/coffee_served.log')
    beverages_served = f.read()
    beverages_served_dict = ast.literal_eval(beverages_served)
    
    print(beverages_served)
    print(type(beverages_served))
    print(beverages_served_dict)
    print(type(beverages_served_dict))
    return beverages_served_dict

# For testing
total_today_served = 120
expresso_today_served = 40
latte_today_served = 60
cappuccino_today_served = 20

def update_beverages_served_lifetime(total_today_served, expresso_today_served, latte_today_served, cappuccino_today_served):
    beverages_served_lifetime = get_beverages_served_lifetime()
    print(beverages_served_lifetime)
    print(beverages_served_lifetime(total_served_lifetime))
    # beverages_served_lifetime.update({"total_served_lifetime": (int("total_served_lifetime") + total_today_served), "expresso_served_lifetime": (int("expresso_served_lifetime") + expresso_today_served), "latte_served_lifetime": (int("latte_served_lifetime") + latte_today_served), "cappuccino_served_lifetime": (int("cappuccino_served_lifetime") + cappuccino_today_served)})
    # print(beverages_served_lifetime)
    # print(type(beverages_served_lifetime))
    # f = open('DAY_015/coffee_machine/reports/coffee_served.log', "w")
    # f.write(beverages_served_lifetime)
    
    
#     f = open('DAY_015/coffee_machine/reports/coffee_served.log')
#     beverages_served = f.read()
#     beverages_served{total_served{}} =    

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

machine_report = {
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
    
# Testing writting to file. It works, Yeehaw.
print(machine_report)
print(datetime.now())
report_file_name = "report_" + str(datetime.now()) + ".log"
f = open("DAY_015/coffee_machine/reports/" + report_file_name, "w")
f.write(str(machine_report))
f.close()
get_beverages_served_lifetime()
update_beverages_served_lifetime(total_today_served,expresso_today_served, latte_today_served, cappuccino_today_served)

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
    # Complete shutdown steps including unload_machine()
    print("Shutdown Procedure")

def build_report():
    report_file_name = "report_" + datetime.now() + ".log"
    f = open(report_file_name, "w")
    f.write(machine_report)
    f.close()

def refill(in_machine_resources):

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

# def http_error(status): # Example of case switch statement
#     match status:
#         case 400:
#             return "Bad request"
#         case 404:
#             return "Not found"
#         case 418:
#             return "I'm a teapot"

#         # If an exact match is not confirmed, this last case will be used if provided
#         case _:
#             return "Something's wrong with the internet"


coffee_emoji = "☕️"




