from os import system
import csv
import json
from datetime import datetime
from twilio.rest import Client

from a_menu import Menu
from a_coffee_machine import CoffeeMaker
from a_money_machine import MoneyMachine
from a_coin_dispenser import CoinDispenser
from a_till import Till
from a_loyalty_service import LoyaltyService
from a_customer import Customer
from a_credit_card import CreditCard
from a_gift_card import GiftCard

from logo import logo

coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()
coin_dispenser = CoinDispenser()
till = Till()
loyalty_service = LoyaltyService()
customer = Customer()
credit_card = CreditCard()
gift_card = GiftCard()

menu = Menu()

is_on = True

while is_on:
    options = menu.get_items()
    print(menu.get_items())
    for drink in menu.get_items():
        drink = menu.find_drink(drink)
        print(f"drink: {drink}")
        if coffee_maker.is_resource_sufficient(drink):
            print(f"{drink.name} is available")
        else:
            menu -= drink
            print(f"{drink.name} is not available")
    choice = input(f"What would you like? ({options}): ")
    if choice == "off":
        is_on = False
    elif choice == "report":
        coffee_maker.report()
        money_machine.report()
    else:
        drink = menu.find_drink(choice)
        
        if coffee_maker.is_resource_sufficient(drink) and money_machine.make_payment(drink.cost):
          coffee_maker.make_coffee(drink)
          money_machine.money_received = 0 # Suggested fix for the bug in the money_machine.py
