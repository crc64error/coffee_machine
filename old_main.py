# Rest in Peace Queen Elizabeth the 2nd of England. May you find rest.
from ast import Pass
from datetime import datetime
from os import system
import json
from logo import logo
from twilio.rest import Client
import smtplib, ssl
import config
import uuid


system('clear')

def json_file_to_dict(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data

############################ Global Variables ############################
##

   
# Beverage Counter
beverage_served_counter = json_file_to_dict('process_records/process_record.json')

# Transaction Record Template
transaction_record = {
    "loyalty_uuid": "",
    "transaction_id": "",
    "transaction_qr_code": "",
    "transaction_type": "",
    "transaction_amount": "",
    "transaction_date": "",
    "transaction_time": "",
    "transaction_status": "",
    "transaction_remarks": "",
    "Date/Time": "",
    "selection_code": "",
    "selection": "",
    "price": 0.0,
    "transaction": {
        "balance": 0,
        "tender_value": 0.0,
        "change": 0.0
    }
}
# In machine ingredients
in_machine_ingredients = {'water': 3000, 'milk': 3000, 'coffee': 1000, 'cups': 200}

# Coins in coin dispenser
coin_dispenser = {'machine_pennies': 50, 'machine_pennies_max': 50, 'machine_nickels': 40, 'machine_nickels_max': 40, 'machine_dimes': 50, 'machine_dimes_max': 50, 'machine_quarters': 40, 'machine_quarters_max': 40, 'machine_halves': 40, 'machine_halves_max': 40, 'machine_dollars': 50, 'machine_dollars_max': 50 }
till_dump = { 'pennies': 0, 'nickels': 0, 'dimes': 0, 'quarters': 0, 'half_dollars': 0, 'small_dollars': 0, "value_in_till": 0.00 }

# Transaction_record carries the load of the work
order = {'Date/Time': '', 'selection_code': '', 'selection': '', 'price': 0.00, 'pennies': 0, 'nickels': 0, 'dimes': 0, 'quarters': 0, 'half_dollars': 0, 'small_dollars': 0, }

value_of_coins = 0.00
value_of_till = 0.00
till_deposit = {'income': 0, 'till': 0}
# Coins in machine
# pennies = 0
# nickels = 0
# dimes = 0
# quarters = 0
# halves = 0
# dollars = 0

sms_enabled = False

############################ Step Thru and Notes #############################
##
# Step 1: On machine boot: 
# 1.1: Load the coin dispenser status from the coin_dispenser.json file
# 1.2: Load the ingredient dispenser status from the ingredient_dispenser.json file
# 1.3: Check Cleaning Status -> If Cleaning is required, cleaning_prompt = True, else cleaning_prompt = False
# 1.4: Check Restock Status -> If Restock is required, refill_prompt = True, else refill_prompt = False
# 1.5: Check Network Status -> If Network is down, network_prompt = True, else network_prompt = False, Notify Staff, SMS, Email
# -1.6: Load Lifetime counters for beverages, ingredients, and coins into local variables
# Step 2: On customer approach:
# 2.1: Present menu for loyalty card
# 2.1.1: If customer has a valid loyalty card
# 2.1.2: Check network for account updates, if updates are found, update local variables in loyalty_customers/loyalty_customers.py {dict}
# 2.1.3: Load loyalty discount to local variable
# 2.2: Check for available beverages -> menu_options
# 2.3: Present menu for beverage selection
# 2.4: Present menu for beverage size
# 2.5: Present menu for beverage extras
# Step 3: On beverage selection:
# 3.0.1: Generate uuid for transaction -> "transaction_id"
# 3.0.2: Generate qr code for transaction -> "transaction_qr_code"
# 3.1: Load cost of beverage and extras to active_transaction_record
# 3.2: Process Payment - coins, debit, iris-scan, apple pay, etc.
# 3.2.1: If coins: Check total_tender_value against beverage_cost
# 3.2.2: If coins over cost, dispense change
# 3.2.3: If coins under cost, present option to return coins
# 3.2.4: If coins under cost, and customer unable to continue, refund coins, start over
# Step 4: On payment complete:
# 4.1: Prepare beverage
# 4.2: Dispense beverage
# 4.3: Update beverage counter, today, and lifetime
# 4.4: Update ingredient dispenser
# 4.5: Print reciept
# 4.6: Update coin dispenser, lifetime, sales, and today
# 5.0: check for cleaning, restock, network
##
############################ End Step Thru and Notes #############################


# # Step 1: On machine boot:
# # 1.1: Load the coin dispenser status from the coin_dispenser.json file
# 1.2: Load the ingredient dispenser status from the ingredient_dispenser.json file
# 1.3: Check Cleaning Status -> If Cleaning is required, cleaning_prompt = True, else cleaning_prompt = False
# 1.4: Check Restock Status -> If Restock is required, refill_prompt = True, else refill_prompt = False
# 1.5: Check Network Status -> If Network is down, network_prompt = True, else network_prompt = False, Notify Staff, SMS, Email
# 1.6: Load Lifetime counters for beverages, ingredients, and coins into local variables
def boot_up():
    print("Boot Up")
    coin_dispenser = json_file_to_dict('process_records/coin_dispenser.json')
    check_coin_dispenser(coin_dispenser)    
    machine_consumables = json_file_to_dict('process_records/machine_consumables.json')
    cleaning_prompt = json_file_to_dict('process_records/process_record.json')['cleaning_prompt']
    refill_prompt = json_file_to_dict('process_records/process_record.json')['refill_prompt']
    served_since_cleaning = json_file_to_dict('process_records/process_record.json')['beverages_served']['served_since_cleaning'] # if greater than 20, machine needs cleaned at open.
    served_since_refill = json_file_to_dict('process_records/process_record.json')['beverages_served']['served_since_refill'] # if greater than 20, machine needs restocked at open.
    if served_since_cleaning > 20:
        cleaning_prompt = True
        note_to_management = "Machine needed cleaned at open."
        send_operational_alert(note_to_management)
    if served_since_refill > 20:
        note_to_management = "Machine needed restocked at open."
        send_operational_alert(note_to_management)
    network_test(boot_up=True)
    if network_test == "Pass":
        offline_prompt = False
    else:
        network_test = "Failed"
        offline_prompt = True
        note_to_management = "Network down at open."
        send_operational_alert(note_to_management)
    
    menu(machine_consumables, coin_dispenser, cleaning_prompt, refill_prompt, offline_prompt)
        
        
def check_coin_dispenser(coin_dispenser):
    coin_prompt = False
    if coin_dispenser['pennies'] < 50:
        note_to_management = "Pennies low"
        coin_prompt = True
    elif coin_dispenser['nickels'] < 30:
        note_to_management = "Nickels low"
        coin_prompt = True
    elif coin_dispenser['dimes'] < 30:
        note_to_management = "Dimes low"
        coin_prompt = True
    elif coin_dispenser['quarters'] < 30:
        note_to_management = "Quarters low"
        coin_prompt = True
    elif coin_dispenser['half_dollars'] < 30:
        note_to_management = "Half Dollars low"
        coin_prompt = True
    elif coin_dispenser['dollars'] < 30:
        note_to_management = "Dollars low"
        coin_prompt = True
    send_operational_alert(note_to_management)
    return coin_prompt
    
def send_operational_alert(note_to_management):
    print("Send Operational Alert")
    if sms_enabled:
        send_sms(note_to_management)
    send_email(note_to_management)
    
def send_sms(sms_enabled, sms_message):
    if sms_enabled == True:
        account_sid = config.account_sid
        auth_token = config.auth_token
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            body=sms_message,
            from_=config.from_number,
            to=config.to_number
        )
        print(message.sid)
        account_sid = config.account_sid 
        auth_token = config.auth_token 
        client = Client(account_sid, auth_token) 
    
        message = client.messages.create(   
            messaging_service_sid= config.messaging_service_sid,
            body= sms_message,      
            to=config.account_receiver
        )
        # print(message.sid)
    else:
        print("SMS Disabled, Contact Staff!")
        send_email(sms_enabled, sms_message, sms_enabled)
    sms_records = message.sid

def send_email(sms_enabled, sms_message):
    port = 465  # For SSL
    password = config.email_password

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(config.email_server, port, context=context) as server:
        server.login(config.service_email, config.email_password)

# Step 2: On customer approach:
# 2.1: Present menu for loyalty card
# 2.1.1: If customer has a valid loyalty card
# 2.1.2: Check network for account updates, if updates are found, update local variables in loyalty_customers/loyalty_customers.py {dict}
# 2.1.3: Load loyalty discount to local variable
# 2.2: Check for available beverages -> menu_options
# 2.3: Present menu for beverage selection
# 2.4: Present menu for beverage size
# 2.5: Present menu for beverage extras

# Do you have a loyalty Card? Yes/No
def check_discount(loyalty_card):
    loyalty_discount = max(loyalty_card['number_of_visits_in_last_year'] * 0.1, 30) # 30% discount is the max, 300 visits in a year, generous.
    return loyalty_discount

def menu(machine_consumables, coin_dispenser, cleaning_prompt, refill_prompt, offline_prompt):
    while cleaning_prompt == False and refill_prompt == False and offline_prompt == False:
        print("Menu")
        print("Do you have a loyalty card? Yes/No")
        loyalty_card = input("Scan your loyalty card or type 'No' if you do not have one: ") # For pretend, a loyalty card is the member id
        loyalty_accounts = json_file_to_dict('loyalty_customers/loyalty_customers.json')
        if loyalty_card in loyalty_accounts:
            print("Loyalty Card Accepted")
            loyalty_card = loyalty_accounts['Customers'][loyalty_card]
            loyalty_discount = check_discount(loyalty_card)
            print("Your loyalty discount is: " + str(loyalty_discount) + "%")
        elif loyalty_card == "No":
            loyalty_card = False
            loyalty_discount = 0
            print("Sign up for a loyalty account with the qrcode on your receipt!")
        else:
            print("Invalid Input")
        menu_options = []  # Starting point for tomorrow
        for beverage in machine_consumables:
            if machine_consumables[beverage]['available'] == True:
                menu_options.append(beverage)
        print("Menu Options: ", menu_options)
        print("What would you like to order?")
        beverage = input()
        if beverage in menu_options:
            print("Beverage Selected: ", beverage)
        else:
            print("Invalid Input")
            menu(machine_consumables, coin_dispenser, cleaning_prompt, refill_prompt, offline_prompt)
        print("What size would you like?")
        size = input()
        if size in machine_consumables[beverage]['sizes']:
            print("Size Selected: ", size)
        else:
            print("Invalid Input")
            menu(machine_consumables, coin_dispenser, cleaning_prompt, refill_prompt, offline_prompt)
        print("Would you like any extras?")
        extras = input()
        if extras in machine_consumables[beverage]['extras']:
            print("Extras Selected: ", extras)
        else:
            print("Invalid Input")
            menu(machine_consumables, coin_dispenser, cleaning_prompt, refill_prompt, offline_prompt)
        print("Please insert coins")
        # payment(machine_consumables, coin_dispenser, beverage, size, extras, loyalty_card, loyalty_discount)
    print("Menu")
    menu_options = json_file_to_dict('menu_options.json')
    menu_options = menu_options['menu_options']
    print(menu_options)
    menu_selection = input("Please select a beverage: ")
    if menu_selection == "1":
        print("You selected a small coffee")
        beverage = "coffee"
        size = "small"
        extras = "none"
        return beverage, size, extras
    elif menu_selection == "2":
        print("You selected a medium coffee")
        beverage = "coffee"
        size = "medium"
        extras = "none"
        return beverage, size, extras
    elif menu_selection == "3":
        print("You selected a large coffee")
        beverage = "coffee"
        size = "large"
        extras = "none"
        return beverage, size, extras
    elif menu_selection == "4":
        print("You selected a small tea")
        beverage = "tea"
        size = "small"
        extras = "none"
        return beverage, size, extras
    elif menu_selection == "5":
        print("You selected a medium tea")
        beverage = "tea"
        size = "medium"
        extras = "none"
        return beverage, size, extras
    elif menu_selection == "6":
        print("You selected a large tea")
        beverage = "tea"
        size = "large"
        extras = "none"
        return beverage, size, extras
    elif menu_selection == "7":
        print("You selected a small soda")
        beverage = "soda"
        size = "small"
        extras = "none"
        return beverage, size, extras
    elif menu_selection == "8":
        print("You selected a medium soda")
        beverage = "soda"
        size = "medium"
        extras = "none"
        return beverage, size, extras
    elif menu_selection == "9":
        print("You selected a large soda")
        beverage = "soda"
        size = "large"
        extras = "none"
        return beverage, size, extras
    elif menu_selection == "10":
        print("You selected a small juice")
        beverage = "juice"
        size = "small"
        extras = "none"
        return beverage, size, extras
    elif menu_selection == "11":
        print("You selected a medium juice")
        beverage = "Unknown"

def menu_old(machine_consumables, coin_dispenser, cleaning_prompt, refill_prompt, offline_prompt, sms_enabled):
    # Populate the menu with the available beverages
    if machine_consumables['coffee'] <= 500 or machine_consumables['milk'] <= 1000 or machine_consumables['water'] <= 1000 or machine_consumables['cups'] <= 40 or machine_consumables['chocolate'] <= 500 or machine_consumables['vanilla'] <= 100 or machine_consumables['honey'] <= 100:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, please restock!")
    if machine_consumables['water'] <= 400 and machine_consumables['water'] > 350:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, water is low, please restock!")
    elif machine_consumables['water'] <= 350:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, water is empty, machine is disabled!")
        
    if machine_consumables['coffee'] <= 200 and machine_consumables['coffee'] > 64:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, coffee is low, please restock!")
    elif machine_consumables['coffee'] <= 64:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, coffee is empty, machine is disabled!")
        
    if machine_consumables['milk'] <= 600 and machine_consumables['milk'] > 150:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, milk is low, please restock!")
    elif machine_consumables['milk'] <= 150:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, milk is empty, machine is disabled!")
        latte = False
        Vanilla_Cappuccino = False
        Caramel_Cappuccino = False
        Cortado = False
        mocha = False
        
    if machine_consumables['cups'] <= 20 and machine_consumables['cups'] > 5:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, cups are low, please restock!")
    elif machine_consumables['cups'] <= 5:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, cups are empty, machine is disabled!")
        
    if machine_consumables['chocolate'] <= 100 and machine_consumables['chocolate'] > 20:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, chocolate is low, please restock!")
    elif machine_consumables['chocolate'] <= 20:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, chocolate is empty, Mocha is disabled!")
        mocha = False
    
    if machine_consumables['vanilla'] <= 20 and machine_consumables['vanilla'] > 5:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, vanilla is low, please restock!")
    elif machine_consumables['vanilla'] <= 5:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, vanilla is empty, Vanilla Cappuccino is disabled!")
        vanilla_cappuccino = False
    
    if machine_consumables['honey'] <= 20 and machine_consumables['honey'] > 5:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, honey is low, please restock!")
    elif machine_consumables['honey'] <= 5:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, honey is empty, Cortado is disabled!")
        cortado = False
    
    if machine_consumables['caramel'] <= 40 and machine_consumables['caramel'] > 10:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, caramel is low, please restock!")
    elif machine_consumables['caramel'] <= 10:
        contact_staff(sms_enabled, sms_message="Coffee Machine needs attemtion, caramel is empty, Caramel Cappuccino is disabled!")
        caramel_cappuccino = False
        

        
def contact_staff(sms_enabled, sms_message):
    print("Please contact a staff member.")
    send_sms(sms_enabled, sms_message, sms_enabled)
    send_email()
    staff_contacted = True
    while staff_contacted == True:
        staff_contacted = input("Has a staff member been contacted? (y/n): ")
        if staff_contacted == "y":
            staff_contacted = False
            print("Thank you.")
        elif staff_contacted == "n":
            staff_contacted = True
            print("Please contact a staff member.")
        else:
            staff_contacted = True
            print("Please enter 'y' or 'n'.")
    return staff_contacted

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
    json_dict = json.dumps(beverages_served_lifetime, indent=4)
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
    
    
def check_tender(transaction_record, refill_prompt):
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
        
def give_change(transaction_record, coin_dispenser, refill_prompt):
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

    
def prepare_beverage(transaction_record, in_machine_ingredients, beverage_served_counter, cleaning_prompt, refill_prompt):
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
    json_dict = json.dumps(transaction_record, indent=4)
    f.write(json_dict)
    f.write(",\n")
    json_dict = json.dumps(till_deposit, indent=4)
    f.write(json_dict)
    f.write(",\n")
    json_dict = json.dumps(till_dump, indent=4)
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
# cleaning_prompt = False
# refill_prompt = False
# have_an_espresso = True
# have_a_late = True
# have_a_cappuccino = True

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
    json_dict = json.dumps(coin_dispenser_report, indent=4)
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
        
    
coffee_emoji = "☕️"

############################################################################################################
####### Learning Reference Area 
############################################################################################################

# # Dealing with nested Dicts
# people = {1: {'Name': 'John', 'Age': '27', 'Sex': 'Male'},
#           2: {'Name': 'Marie', 'Age': '22', 'Sex': 'Female'}}

# for p_id, p_info in people.items():
#     print("\nPerson ID:", p_id)
    
#     for key in p_info:
#         print(key + ':', p_info[key])


# # File handling
# report_file_name = "report_" + str(datetime.now()) + ".log"

# w to write, w+ to create or write, 
# File access mode ‘a+’, creates opens the file for both read and writing. Also if file it doesn’t exist, and then it creates the file too.
# f = open("reports/" + report_file_name, "w") 

# f.write(str(machine_report))

# f.close()

# For initial setup of machine
# def create_a_json(total_served_today, espresso_served_today, latte_served_today, cappuccino_served_today):
#     """create file for beverages served

#     Args:
#         total_served_today (int): total of all beverages
#         espresso_served_today (int): total of espressos
#         latte_served_today (int): total of lattes
#         cappuccino_served_today (int): total of cappuccinos
#     """
#     beverages_served = {"total_served_lifetime": total_served_today, "espresso_served_lifetime": espresso_served_today, "latte_served_lifetime": latte_served_today, "cappuccino_served_lifetime": cappuccino_served_today }
    
#     json_dict = json.dumps(beverages_served, indent = 4)
#     f = open('reports/coffee_served.json', 'w')
#     f.write(json_dict)
#     f.close()