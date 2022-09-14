from a_menu import Menu
from a_coffee_machine import CoffeeMaker
from a_money_machine import MoneyMachine
from logo import logo

money_machine = MoneyMachine()
coffee_maker = CoffeeMaker()
menu = Menu()

is_on = True

while is_on:
    options = menu.get_items() # Update to show drinks available with available ingredients.
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
          money_machine.momney_received = 0 # Suggested fix for the bug in the money_machine.py
