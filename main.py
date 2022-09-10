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
# from menu import MENU
# from resources import resources
# from coins import coins # Till quantities to provide change: Pennies, nickels, dimes, quarters, half-dollars, small-dollars


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
espresso_served_today = 0
latte_served_today = 0
cappuccino_served_today = 0
in_machine_till = 0.00
in_machine_coin_dispenser = 0
in_machine_water = 0
in_machine_milk = 0
in_machine_coffee = 0
in_machine_cups = 0
# Coins in coin dispenser
machine_pennies = 0
machine_nickles = 0
machine_dimes = 0
machine_quarters = 0
machine_halves = 0
machine_dollars = 0

value_of_coins = 0.00
value_of_till = 0.00
till_deposit = 0.00
# Coins in machine
pennies = 0
nickels = 0
dimes = 0
quarters = 0
halves = 0
dollars = 0

# For initial setup of machine
def create_a_json(total_served_today, espresso_served_today, latte_served_today, cappuccino_served_today):
    """create file for beverages served

    Args:
        total_served_today (int): total of all beverages
        espresso_served_today (int): total of espressos
        latte_served_today (int): total of lattes
        cappuccino_served_today (int): total of cappuccinos
    """
    beverages_served = {"total_served_lifetime": total_served_today, "espresso_served_lifetime": espresso_served_today, "latte_served_lifetime": latte_served_today, "cappuccino_served_lifetime": cappuccino_served_today }
    
    json_dict = json.dumps(beverages_served)
    f = open('reports/coffee_served.json', 'w')
    f.write(json_dict)
    f.close()

# Get the value of coins for reports and refilling the coin dispenser
def get_value_of_coins(pennies, nickels, dimes, quarters, halves, dollars):
    value_of_coins = 0.00
    value_of_coins = (pennies * .01) + (nickels * .05) + (dimes * .1) + (quarters * .25) + (halves * .5) + (dollars * 1)
    return value_of_coins

def get_beverages_served_lifetime():
    """ Get lifetime counts of beverages served

    Returns:
        dict: The count of all beverages served by this machine for life.
    """
    
    # We open the file and save it as a local dictionary, passed as beverages_served_dict on return.
    with open('reports/coffee_served.json') as json_file:
        beverages_served_dict = json.load(json_file)
    return beverages_served_dict

def update_beverages_served_lifetime(total_served_today, espresso_served_today, latte_served_today, cappuccino_served_today):
    """Update lifetime count of beverages served

    Args:
        total_served_today (int): int
        espresso_served_today (int): int
        latte_served_today (int): int
        cappuccino_served_today (int): int
    """
    # We grab the dictionary, beverages_served_lifetime, and add the values from total_served_today, espresso_served_today, latte_served_today and cappuccino_served_today
    # We then update the local dict with the new values and write the dictionary to json file as json
    beverages_served_lifetime = get_beverages_served_lifetime()
    print(beverages_served_lifetime)
    # This feels messy
    total_served_today = {"total_served_lifetime": (beverages_served_lifetime.get("total_served_lifetime") + total_served_today)}
    espresso_served_today = {"espresso_served_lifetime": (beverages_served_lifetime.get("espresso_served_lifetime") + espresso_served_today)}
    latte_served_today = {"latte_served_lifetime": (beverages_served_lifetime.get("latte_served_lifetime") + latte_served_today)}
    cappuccino_served_today = {"cappuccino_served_lifetime": (beverages_served_lifetime.get("cappuccino_served_lifetime") + cappuccino_served_today)}
    beverages_served_lifetime.update(total_served_today)
    beverages_served_lifetime.update(espresso_served_today)
    beverages_served_lifetime.update(latte_served_today)
    beverages_served_lifetime.update(cappuccino_served_today)
    # Write the file
    json_dict = json.dumps(beverages_served_lifetime)
    f = open('reports/coffee_served.json', 'w')
    f.write(json_dict)
    f.close()
    
def update_espresso_served_today(total_served_today, espresso_served_today):
    """ Increment values, total_served_today, espresso_served_today

    Args:
        total_served_today (int): total beverages served today
        espresso_served_today (int): total espresso served today

    Returns:
        total_served_today (int): total beverages served today
        espresso_served_today (int): total espresso served today
    """
    total_served_today += 1
    espresso_served_today += 1
    return total_served_today, espresso_served_today
  
def update_latte_served_today(total_served_today, latte_served_today):
    total_served_today += 1
    latte_served_today += 1
    return total_served_today, latte_served_today

def update_cappuccino_served_today(total_served_today, cappuccino_served_today):
    total_served_today += 1
    cappuccino_served_today += 1
    return total_served_today, cappuccino_served_today

def check_for_cleaning(total_served_today):
    if total_served_today > 200:
        cleaning_prompt = True

def check_for_restock(in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups):
    if in_machine_water < 500:
        refill = True
    elif in_machine_milk < 300:
        refill = True
    elif in_machine_coffee < 48:
        refill = True
    elif in_machine_cups < 5:
        refill = True
    
def start_a_transaction(refill):
    while refill is not True:
        selection_code = input("Would you like an (E)xpresso, (L)atte or (C)appuccino").lower() # Technically, this would be three individual buttons, but, you know.
        if selection_code == "e":
            selection = "espresso"
        elif selection_code == "l":
            selection = "latte"
        elif selection_code == "c":
            selection = "cappuccino"
        elif selection_code == "cleaning":
            selection = "cleaning"
        elif selection_code == "refill":
            selection = "refill"
        elif selection_code == "coins":
            selection = "till"
        elif selection_code == "shutdown":
            selection = "shutdown"
        else:
            print("The employee is out of order. Please try again.")
            start_a_transaction()
        return selection
    print("Machine is waiting for a refill, please alert staff.")

def check_transaction_for_service_entries(selection):
    if selection ==  "espresso" or selection == "latte" or selection == "cappuccino":
        price_a_transaction(selection)
    elif selection == "cleaning":
        clean_machine()
    elif selection == "refill":
        refill_machine()
    elif selection == "till":
        refill_coin_dispenser
    elif selection == "shutdown":
        shutdown_machine()

def price_a_transaction(selection):
    if selection == "espresso":
        cost = espresso_cost
    elif selection == "latte":
        cost = latte_cost
    elif selection == "cappuccino":
        cost = cappuccino_cost
    make_some_money(cost, selection)

def make_some_money(cost, selection):
    print(f"Your price for your {selection} is ${'{0:.2f}'.format(cost)}. Insert coin(s)")
    coins_in = { "pennies": 0, "nickels": 0, "dimes": 0, "quarters": 0, "half_dollars": 0, "small_dollars": 0 }
    coins_in["dollars"] = int(input("Dollar Coins: "))
    coins_in["half_dollars"] = int(input("Half Dollar Coins: "))
    coins_in["quarters"] = int(input("Quarters: "))
    coins_in["dimes"] = int(input("Dimes: "))
    coins_in["nickels"] = int(input("Nickels: "))
    coins_in["pennies"] = int(input("Pennies: "))
    check_tender(coins_in, cost)
    
    
def check_tender(coins_in, cost, selection):
    get_value_of_coins(coins_in)
    if value_of_coins < cost:
        cost -= value_of_coins
        make_some_money(cost, selection)
    elif value_of_coins > cost:
        change = value_of_coins - cost
        give_change(change, cost, selection)
    elif value_of_coins == cost:
        prepare_beverage(selection)
        
def give_change(change, cost, selection):
    print("give_change")
    while change >= 1.00 and machine_dollars > 0:
        print("Dispensing Dollar Coin")
        change -= 1
        machine_dollars -= 1
    while change >= .50 and machine_halves > 0:
        print("Dispensing half dollars")
        change -= .5
        machine_halves -= 1
    while change >= .25 and machine_quarters > 0:
        print("Dispensing quarters")
        change -= .25
        machine_quarters -= 1
    while change >= .1 and machine_dimes > 0:
        print("Dispensing dimes")
        change -= .1
        machine_dimes -= 1
    while change >= .05 and machine_nickles > 0:
        print("Dispensing nickels")
        change -= .05
        machine_nickles -= 1
    while change >= .01 and machine_pennies > 0:
        print("Dispensing pennies")
        change -= .01
        machine_pennies -= 1
    if change > 0: 
        print(f"Machine ran out of change, please wait for your beverage, then see a cashier, and tell them you are owed {change}")
        cleaning_prompt = True
    prepare_beverage(selection)

    
def prepare_beverage(selection):
    print("prepare_beverage")
    if selection == "espresso":
        water = espresso_recipe['water']
        milk = espresso_recipe['milk']
        coffee = espresso_recipe['coffee']
        in_machine_water -= water
        in_machine_milk -= milk
        in_machine_coffee -= coffee
        in_machine_cups -= 1
        total_served_today += 1
        espresso_served_today += 1
        print("Your delicious hot and fresh espresso is ready. Enjoy")
        check_for_cleaning(total_served_today)
        check_for_restock(in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups)
    
    if selection == "latte":
        water = latte_recipe['water']
        milk = latte_recipe['milk']
        coffee = latte_recipe['coffee']
        in_machine_water -= water
        in_machine_milk -= milk
        in_machine_coffee -= coffee
        in_machine_cups -= 1
        total_served_today += 1
        latte_served_today += 1
        print("Your delicious hot and fresh latte is ready. Enjoy")
        check_for_cleaning(total_served_today)
        check_for_restock(in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups)
        
    if selection == "cappuccino":
        water = cappuccino_recipe['water']
        milk = cappuccino_recipe['milk']
        coffee = cappuccino_recipe['coffee']
        in_machine_water -= water
        in_machine_milk -= milk
        in_machine_coffee -= coffee
        in_machine_cups -= 1
        total_served_today += 1
        cappuccino_served_today += 1
        print("Your delicious hot and fresh Cappuccino is ready. Enjoy")
        check_for_cleaning(total_served_today)
        check_for_restock(in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups)
    

# Menu Toggles Should be False on boot for initial setup
cleaning_prompt = True
have_an_espresso = False
have_a_late = False
have_a_cappuccino = False

# in_machine_resources
def get_in_machine_quantities(in_machine_till, in_machine_coin_dispenser, in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups, machine_nickles, machine_dimes, machine_quarters, machine_halves, machine_dollars):
    # If booting
    # get file in_machine_resources.json and safe local variables
    #   in_machine_till
    #   in_machine_coin_dispenser{pennies, nickels, dimes, quarters, half_dollars, small_dollars}
    #   in_machine_water
    #   in_machine_milk
    #   in_machine_coffee
    #   in_machine_cups
    with open('in_machine_quantities.json') as json_file:
        in_machine_quantities_dict = json.load(json_file)
        in_machine_till = in_machine_quantities_dict['till']
        in_machine_coin_dispenser = in_machine_quantities_dict['change_dispenser']
        in_machine_water = in_machine_quantities_dict['water']
        in_machine_milk = in_machine_quantities_dict['milk']
        in_machine_coffee = in_machine_quantities_dict['coffee']
        in_machine_cups = in_machine_quantities_dict['cups']
        machine_pennies = in_machine_coin_dispenser['pennies']
        machine_nickles = in_machine_coin_dispenser['nickels']
        machine_dimes = in_machine_coin_dispenser['dimes']
        machine_quarters = in_machine_coin_dispenser['quarters']
        machine_halves = in_machine_coin_dispenser['half_dollars']
        machine_dollars = in_machine_coin_dispenser['small_dollars']
        
        # Troubleshooting
        print(in_machine_till, in_machine_coin_dispenser, machine_pennies, in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups, machine_nickles, machine_dimes, machine_quarters, machine_halves, machine_dollars)
        
        
    # json_dict = json.dumps(beverages_served_lifetime)
    # f = open('reports/coffee_served.json', 'w')
    # f.write(json_dict)
    # f.close()
    # return beverages_served_dict
    
    return in_machine_till, in_machine_coin_dispenser, in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups, machine_nickles, machine_dimes, machine_quarters, machine_halves, machine_dollars

def till_in(till_deposit, report_pennies, report_nickels, report_dimes, report_quarters, report_halves, report_dollars):
    value_of_coins = get_value_of_coins(report_pennies, report_nickels, report_dimes, report_quarters, report_halves, report_dollars)
    till_deposit += value_of_coins
    report_pennies = 0
    report_nickels = 0
    report_dimes = 0
    report_quarters = 0
    report_halves = 0
    report_dollars = 0
    return till_deposit, report_pennies, report_nickels, report_dimes, report_quarters, report_halves, report_dollars
    

def till_out(till_deposit):
    print("Till out")
    

def refill_coin_dispenser():
    with open('coins.json') as json_file:
        max_coin_dispenser = json.load(json_file)
    with open('in_machine_quantities.json') as json_file:
        in_machine_quantities_dict = json.load(json_file)
    
    in_machine_coin_dispenser = in_machine_quantities_dict["change_dispenser"]
        
    max_pennies = max_coin_dispenser["pennies"]
    max_nickels = max_coin_dispenser["nickels"]
    max_dimes = max_coin_dispenser["dimes"]
    max_quarters = max_coin_dispenser["quarters"]
    max_halves = max_coin_dispenser["half_dollars"]
    max_dollars = max_coin_dispenser["small_dollars"]
    machine_pennies = in_machine_coin_dispenser["pennies"]
    machine_nickles = in_machine_coin_dispenser["nickels"]
    machine_dimes = in_machine_coin_dispenser["dimes"]
    machine_quarters = in_machine_coin_dispenser["quarters"]
    machine_halves = in_machine_coin_dispenser["half_dollars"]
    machine_dollars = in_machine_coin_dispenser["small_dollars"]
    
    report_pennies = max_pennies - machine_pennies
    report_nickels = max_nickels - machine_nickles
    report_dimes = max_dimes - machine_dimes
    report_quarters = max_quarters - machine_quarters
    report_halves = max_halves - machine_halves
    report_dollars = max_dollars - machine_dollars
    
    # Lets set value for the amount of coins in the coin dispenser
    machine_pennies = max_pennies
    machine_nickels = max_nickels
    machine_dimes = max_dimes
    machine_quarters = max_quarters
    machine_halves = max_halves
    machine_dollars = max_dollars
    
    value_of_coins = get_value_of_coins(report_pennies, report_nickels, report_dimes, report_quarters, report_halves, report_dollars)
    
    report_note = input("Input your initials and if any coins were missing, do not leave notes for management: ")
    
    return(machine_pennies, machine_nickels, machine_dimes, machine_quarters, machine_halves, machine_dollars)
    
    # form the dict for the report
    
    coin_dispenser_report = {
        "date_time": str(datetime.now()),
        "money_in": "$"'{0:.2f}'.format(value_of_coins),
        "till_out": "$"'{0:.2f}'.format(till_deposit),
        "note": report_note      
    }
    print(coin_dispenser_report)
    
    # Write the file
    json_dict = json.dumps(coin_dispenser_report)
    report_file_name = "coin_dispenser_report_" + str(datetime.now()) + ".json"
    f = open("reports/" + report_file_name, "w")
    f.write(str(json_dict))
    f.close()
    
    
    

machine_report = { # Template of the machine report
    "used_resources": {
        "water": 0,
        "milk": 0,
        "coffee": 0,
        "cups": 0
    },
    "remaining_resources": {
        "water": 0,
        "milk": 0,
        "coffee": 0
    },
    "sales": {
        "espresso": 0,
        "latte": 0,
        "cappuccino": 0
    },
    "coins_in_till": {
        "pennies": 0,
        "nickels": 0,
        "dimes": 0,
        "quarters": 0,
        "half-dollars": 0,
        "small-dollars": 0
    },
    "coins_in_deposit": {
        "pennies": 0,
        "nickels": 0,
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


# Troubleshooting

with open('menu.json') as json_file:
    menu = json.load(json_file)
    espresso_menu = menu['espresso']
    espresso_recipe = espresso_menu['ingredients']
    espresso_cost = espresso_menu['cost']
    latte_menu = menu['latte']
    latte_recipe = latte_menu['ingredients']
    latte_cost = latte_menu['cost']
    cappuccino_menu = menu['cappuccino']
    cappuccino_recipe = cappuccino_menu['ingredients']
    cappuccino_cost = cappuccino_menu['cost']
    
    # print(menu)
    # print(espresso_menu)
    # print(espresso_recipe)
    # print("$"'{0:.2f}'.format(espresso_cost))

# refill_coin_dispenser()
# get_in_machine_quantities(in_machine_till, in_machine_coin_dispenser, in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups, machine_nickles, machine_dimes, machine_quarters, machine_halves, machine_dollars)
# get_beverages_served_lifetime()
# update_beverages_served_lifetime(total_served_today,espresso_served_today, latte_served_today, cappuccino_served_today)

def boot_machine():
    # Prompt for setup steps
    # Boot the machine
    # Did the machine get cleaned?
    # Did you refill the machine?
    #   If machine was not refilled, get quatities from yesterdays shutdown? current_resources.json
    #   If machine was refilled, refill quantities to max from max_quantities.json
    # Did you empty the till and refill the change dispenser?
        # Our machine has a magic coin handler. If the max amount of pennies it can hold is 50, but is down
        # to 45, but the next customer puts in 10 pennies, 5 will go into the change dispenser and 5 will go
        # in the till.
    # Load menu, recipe, cost file into memory
    
    with open('menu.json.json') as json_file:
        menu = json.load(json_file)
        print(menu)
    
    if bool(input("Clean Machine? ")) ==  True:
        cleaning_prompt = False
    else:
        cleaning_prompt = True
        have_an_espresso = False
        have_a_late = False
        have_a_cappuccino = False
        # Add used resources to report_variable
    
    
    
    if bool(input("Refill machine?")) == True:
        refill_machine()

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

def refill_machine(in_machine_resources):
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
        case "e": # espresso
            if have_an_espresso == True:
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




