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

# Beverage Counter
beverage_served_counter = {'total_served_today': 0, 'espresso_served_today': 0, 'latte_served_today': 0, 'cappuccino_served_today': 0}

in_machine_till = 0.00
in_machine_coin_dispenser = 0

# In machine ingredients
in_machine_ingredients = {'water': 3000, 'milk': 3000, 'coffee': 1000, 'cups': 200}

# Coins in coin dispenser
coin_dispenser = {'machine_pennies': 50, 'machine_pennies_max': 50, 'machine_nickels': 40, 'machine_nickels_max': 40, 'machine_dimes': 50, 'machine_dimes_max': 50, 'machine_quarters': 40, 'machine_quarters_max': 40, 'machine_halves': 40, 'machine_halves_max': 40, 'machine_dollars': 50, 'machine_dollars_max': 50 }
till_dump = { 'pennies': 0, 'nickels': 0, 'dimes': 0, 'quarters': 0, 'half_dollars': 0, 'small_dollars': 0, "value_in_till": 0.00 }

# Transaction_record carries the load of the work
transaction_record = {'Date/Time': '', 'selection_code': '', 'selection': '', 'price': 0.00, 'pennies': 0, 'nickels': 0, 'dimes': 0, 'quarters': 0, 'half_dollars': 0, 'small_dollars': 0, }

value_of_coins = 0.00
value_of_till = 0.00
till_deposit = {'income': 0, 'till': 0}
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
def get_value_of_coins(transaction_record):
    transaction_record['tender'] = (transaction_record['pennies'] * .01) + (transaction_record['nickels'] * .05) + (transaction_record['dimes'] * .1) + (transaction_record['quarters'] * .25) + (transaction_record['half_dollars'] * .5) + (transaction_record['small_dollars'] * 1)
    transaction_record['price'] = transaction_record['price'] - transaction_record['tender']
    refill_or_till(transaction_record, coin_dispenser)
    
    print(transaction_record)
    return transaction_record

def refill_or_till(transaction_record, coin_dispenser):
    # pennies
    if transaction_record['pennies'] > 0:
        while coin_dispenser['machine_pennies'] < coin_dispenser['machine_pennies_max']:
            transaction_record['pennies'] -= 1
            coin_dispenser['machine_pennies'] += 1
        while coin_dispenser['machine_pennies'] == coin_dispenser['machine_pennies_max'] and transaction_record['pennies'] > 0:
            transaction_record['pennies'] -= 1
            till_dump['pennies'] += 1
            till_dump['value_in_till'] += .01
    # Nickels
    if transaction_record['nickels'] > 0:
        while coin_dispenser['machine_nickels'] < coin_dispenser['machine_nickels_max']:
            transaction_record['nickels'] -= 1
            coin_dispenser['machine_nickels'] += 1
        while coin_dispenser['machine_nickels'] == coin_dispenser['machine_nickels_max'] and transaction_record['nickels'] > 0:
            transaction_record['nickels'] -= 1
            till_dump['nickels'] += 1
    # Dimes
    if transaction_record['dimes'] > 0:
        while coin_dispenser['machine_dimes'] < coin_dispenser['machine_dimes_max']:
            transaction_record['dimes'] -= 1
            coin_dispenser['machine_dimes'] += 1
        while coin_dispenser['machine_dimes'] == coin_dispenser['machine_dimes_max'] and transaction_record['dimes'] > 0:
            transaction_record['dimes'] -= 1
            till_dump['dimes'] += 1
    # Quarters
    if transaction_record['quarters'] > 0:
        while coin_dispenser['machine_quarters'] < coin_dispenser['machine_quarters_max']:
            transaction_record['quarters'] -= 1
            coin_dispenser['machine_quarters'] += 1
        while coin_dispenser['machine_quarters'] == coin_dispenser['machine_quarters_max'] and transaction_record['quarters'] > 0:
            transaction_record['quarters'] -= 1
            till_dump['quarters'] += 1
    # Half Dollars
    if transaction_record['half_dollars'] > 0:
        while coin_dispenser['machine_dollars'] < coin_dispenser['machine_dollars_max']:
            transaction_record['half_dollars'] -= 1
            coin_dispenser['machine_dollars'] += 1
        while coin_dispenser['machine_dollars'] == coin_dispenser['machine_dollars_max'] and transaction_record['half_dollars'] > 0:
            transaction_record['half_dollars'] -= 1
            till_dump['half_dollars'] += 1
    # Small Dollars
    if transaction_record['small_dollars'] > 0:
        while coin_dispenser['machine_dollars'] < coin_dispenser['machine_dollars_max']:
            transaction_record['small_dollars'] -= 1
            coin_dispenser['machine_dollars'] += 1
        while coin_dispenser['machine_dollars'] == coin_dispenser['machine_dollars_max'] and transaction_record['small_dollars'] > 0:
            transaction_record['small_dollars'] -= 1
            till_dump['small_dollars'] += 1
    tender_record = till_dump
    till_deposit['income'] += transaction_record['tender']
    till_deposit['till'] += till_dump['value_in_till']
    
    return transaction_record, coin_dispenser, till_deposit, till_dump
    

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
    
def check_for_cleaning(beverage_served_counter):
    if beverage_served_counter['total_served_today'] > 200:
        cleaning_prompt = True

def check_for_restock(in_machine_ingredients):
    if in_machine_ingredients['water'] < 500 or in_machine_ingredients['milk'] < 300 or in_machine_ingredients['coffee'] < 48 or in_machine_ingredients['cups'] < 5:
        refill_prompt = True
    else: 
        refill_prompt = False
    
def start_a_transaction(refill_prompt):
    while refill_prompt is not True:
        transaction_record['Date/Time'] = str(datetime.now())
        transaction_record['selection_code'] = input("Would you like an (E)xpresso, (L)atte or (C)appuccino: ").lower() # Technically, this would be three individual buttons, but, you know.
        if transaction_record['selection_code'] == "e":
            transaction_record['selection'] = "espresso"
        elif transaction_record['selection_code'] == "l":
            transaction_record['selection'] = "latte"
        elif transaction_record['selection_code'] == "c":
            transaction_record['selection'] = "cappuccino"
        elif transaction_record['selection_code'] == "cleaning":
            transaction_record['selection'] = "cleaning"
        elif transaction_record['selection_code'] == "refill":
            transaction_record['selection'] = "refill"
        elif transaction_record['selection_code'] == "coins":
            transaction_record['selection'] = "till"
        elif transaction_record['selection_code'] == "shutdown":
            transaction_record['selection'] = "shutdown"
        else:
            print("The employee is out of order. Please try again.")
            start_a_transaction()
        check_transaction_for_service_entries(transaction_record)
    print("Machine is waiting for a refill, please alert staff.")

def check_transaction_for_service_entries(transaction_record):
    if transaction_record['selection'] ==  "espresso" or transaction_record['selection'] == "latte" or transaction_record['selection'] == "cappuccino":
        price_a_transaction(transaction_record)
    elif transaction_record['selection'] == "cleaning":
        clean_machine()
    elif transaction_record['selection'] == "refill":
        refill_machine()
    elif transaction_record['selection'] == "till":
        refill_coin_dispenser
    elif transaction_record['selection'] == "shutdown":
        shutdown_machine()

def price_a_transaction(transaction_record):
    if transaction_record['selection'] == "espresso":
        transaction_record['price'] = espresso_cost
        transaction_record['balance'] = espresso_cost
    elif transaction_record['selection'] == "latte":
        transaction_record['price'] = latte_cost
        transaction_record['balance'] = latte_cost
    elif transaction_record['selection'] == "cappuccino":
        transaction_record['price'] = cappuccino_cost
        transaction_record['balance'] = cappuccino_cost
    print(f"price_a_transaction: {transaction_record}")
    make_some_money(transaction_record)

def make_some_money(transaction_record):
    print(f"Your price for your {transaction_record['selection']} is ${'{0:.2f}'.format(transaction_record['price'])}. Insert coin(s)")
    print(transaction_record)
    transaction_record["small_dollars"] = int(input("Dollar Coins: "))
    transaction_record["half_dollars"] = int(input("Half Dollar Coins: "))
    transaction_record["quarters"] = int(input("Quarters: "))
    transaction_record["dimes"] = int(input("Dimes: "))
    transaction_record["nickels"] = int(input("Nickels: "))
    transaction_record["pennies"] = int(input("Pennies: "))
    print(f"make_some_money: {transaction_record}")
    check_tender(transaction_record)
    
    
def check_tender(transaction_record):
    get_value_of_coins(transaction_record)
    if transaction_record['tender'] < transaction_record['price']:
        transaction_record['balance'] = transaction_record['price'] - transaction_record['tender']
        make_some_money(transaction_record)
    elif transaction_record['tender'] > transaction_record['price']:
        transaction_record['balance'] = 0
        transaction_record['change'] = transaction_record['tender'] - transaction_record['price']
        give_change(transaction_record, coin_dispenser)
    elif transaction_record['tender'] == transaction_record['price']:
        prepare_beverage(transaction_record, in_machine_ingredients, beverage_served_counter, refill_prompt)
    print(f"check_tender: {transaction_record}")
        
def give_change(transaction_record, coin_dispenser):
    print("give_change")
    change = transaction_record['change']
    while change >= 1.00 and coin_dispenser['machine_dollars'] > 0:
        print("Dispensing Dollar Coin")
        change -= 1
        coin_dispenser['machine_dollars'] -= 1
    while change >= .50 and coin_dispenser['machine_halves'] > 0:
        print("Dispensing half dollars")
        change -= .5
        coin_dispenser['machine_halves'] -= 1
    while change >= .25 and coin_dispenser['machine_quarters'] > 0:
        print("Dispensing quarters")
        change -= .25
        coin_dispenser['machine_quarters'] -= 1
    while change >= .1 and coin_dispenser['machine_dimes'] > 0:
        print("Dispensing dimes")
        change -= .1
        coin_dispenser['machine_dimes'] -= 1
    while change >= .05 and coin_dispenser['machine_nickels'] > 0:
        print("Dispensing nickels")
        change -= .05
        coin_dispenser['machine_nickels'] -= 1
    while change >= .01 and coin_dispenser['machine_pennies'] > 0:
        print("Dispensing pennies")
        change -= .01
        coin_dispenser['machine_pennies'] -= 1
    if change > 0: 
        print(f"Machine ran out of change, please wait for your beverage, then see a cashier, let them know you are owed {change}")
        cleaning_prompt = True
    print(f"give_change: {transaction_record}")
    prepare_beverage(transaction_record, in_machine_ingredients, beverage_served_counter, refill_prompt, till_deposit, till_dump)

    
def prepare_beverage(transaction_record, in_machine_ingredients, beverage_served_counter, refill_prompt):
    print("prepare_beverage")
    if transaction_record['selection'] == "espresso":
        print(espresso_menu)
        water = espresso_recipe['water']
        milk = espresso_recipe['milk']
        coffee = espresso_recipe['coffee']
        in_machine_ingredients['water'] -= water
        in_machine_ingredients['milk'] -= milk
        in_machine_ingredients['coffee'] -= coffee
        in_machine_ingredients['cups'] -= 1
        beverage_served_counter['total_served_today'] += 1
        beverage_served_counter['espresso_served_today'] += 1
        print("Your delicious hot and fresh espresso is ready. Enjoy")
        check_for_cleaning(beverage_served_counter)
        check_for_restock(in_machine_ingredients)
    
    elif transaction_record['selection'] == "latte":
        water = latte_recipe['water']
        milk = latte_recipe['milk']
        coffee = latte_recipe['coffee']
        in_machine_ingredients['water'] -= water
        in_machine_ingredients['milk'] -= milk
        in_machine_ingredients['coffee'] -= coffee
        in_machine_ingredients['cups'] -= 1
        beverage_served_counter['total_served_today'] += 1
        beverage_served_counter['latte_served_today'] += 1
        print("Your delicious hot and fresh latte is ready. Enjoy")
        check_for_cleaning(beverage_served_counter)
        check_for_restock(in_machine_ingredients)
        
    elif transaction_record['selection'] == "cappuccino":
        water = cappuccino_recipe['water']
        milk = cappuccino_recipe['milk']
        coffee = cappuccino_recipe['coffee']
        in_machine_ingredients['water'] -= water
        in_machine_ingredients['milk'] -= milk
        in_machine_ingredients['coffee'] -= coffee
        in_machine_ingredients['cups'] -= 1
        beverage_served_counter['total_served_today'] += 1
        beverage_served_counter['cappuccino_served_today'] += 1
        print("Your delicious hot and fresh Cappuccino is ready. Enjoy")
        check_for_cleaning(beverage_served_counter)
        check_for_restock(in_machine_ingredients)
        
    # Add transaction_record as json to a transaction json file
    # We need to create or open a file named transaction_records_09-11-2022.json
    # We then need to start adding transaction records to the file
    # At shutdown, the file needs to be emailed to the admin address, along with other report files.
    
    print('open')
    date = datetime.now()
    date = date.strftime("%d-%m-%Y")
    f = open('reports/transaction_records_' + date + '.json', 'a+')
    f.write(",\n")
    json_dict = json.dumps(transaction_record)
    f.write(json_dict)
    f.write(",\n")
    json_dict = json.dumps(till_deposit)
    f.write(json_dict)
    f.write(",\n")
    json_dict = json.dumps(till_dump)
    f.write(json_dict)
    f.write(",\n")
    f.close()
    transaction_record = { "Date/Time": "", "selection_code": "", "selection": "", "price": 0, "pennies": 0, "nickels": 0, "dimes": 0, "quarters": 0, "half_dollars": 0, "small_dollars": 0, "balance": 0, "tender": 0, "change": 0}
    # print(f"prepare_beverage: {transaction_record}")
    if cleaning_prompt == False and refill_prompt == False:
        start_a_transaction(refill_prompt) # Change this later depending on machine state after the last transaction
    elif cleaning_prompt == True and refill_prompt == False:
        print("Machine needs to be cleaned, please inform staff.")
    elif cleaning_prompt == False and refill_prompt == True:
        print("Machine is in need of refill, please inform staff.")
    elif cleaning_prompt == True and refill_prompt == True:
        print("Machine is in need of maintenance, please inform staff.")
    

    

# Menu Toggles Should be False on boot for initial setup
cleaning_prompt = False
refill_prompt = False
have_an_espresso = True
have_a_late = True
have_a_cappuccino = True

# in_machine_resources
def get_in_machine_quantities(in_machine_till, in_machine_coin_dispenser, in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups, machine_nickels, machine_dimes, machine_quarters, machine_halves, machine_dollars):
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
        machine_nickels = in_machine_coin_dispenser['nickels']
        machine_dimes = in_machine_coin_dispenser['dimes']
        machine_quarters = in_machine_coin_dispenser['quarters']
        machine_halves = in_machine_coin_dispenser['half_dollars']
        machine_dollars = in_machine_coin_dispenser['small_dollars']
        
        # Troubleshooting
        print(in_machine_till, in_machine_coin_dispenser, machine_pennies, in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups, machine_nickels, machine_dimes, machine_quarters, machine_halves, machine_dollars)
        
        
    # json_dict = json.dumps(beverages_served_lifetime)
    # f = open('reports/coffee_served.json', 'w')
    # f.write(json_dict)
    # f.close()
    # return beverages_served_dict
    
    return in_machine_till, in_machine_coin_dispenser, in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups, machine_nickels, machine_dimes, machine_quarters, machine_halves, machine_dollars

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
    machine_nickels = in_machine_coin_dispenser["nickels"]
    machine_dimes = in_machine_coin_dispenser["dimes"]
    machine_quarters = in_machine_coin_dispenser["quarters"]
    machine_halves = in_machine_coin_dispenser["half_dollars"]
    machine_dollars = in_machine_coin_dispenser["small_dollars"]
    
    report_pennies = max_pennies - machine_pennies
    report_nickels = max_nickels - machine_nickels
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
    "transaction_record_till": {
        "pennies": 0,
        "nickels": 0,
        "dimes": 0,
        "quarters": 0,
        "half-dollars": 0,
        "small-dollars": 0
    },
    "transaction_record_deposit": {
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



start_a_transaction(refill_prompt = False)
# refill_coin_dispenser()
# get_in_machine_quantities(in_machine_till, in_machine_coin_dispenser, in_machine_water, in_machine_milk, in_machine_coffee, in_machine_cups, machine_nickels, machine_dimes, machine_quarters, machine_halves, machine_dollars)
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




