from a_menu import MenuItem


class CoffeeMaker:
    """ Model for the coffee machine """
    def __init__(self):
        self.resources = {
            "water": 20000,
            "milk": 5, # This machine needs a temperature monitor for the stored milk
            "coffee": 3000,
            "chocolate": 5, # 500
            "vanilla": 500,
            "caramel": 500,
            "honey": 100,
            "cups": 500
        }

    def report(self):
        """Prints a report of all resources."""
        print(f"Water: {self.resources['water']}ml")
        print(f"Milk: {self.resources['milk']}ml")
        print(f"Coffee: {self.resources['coffee']}g")
        print(f"Chocolate: {self.resources['chocolate']}g")
        print(f"Vanilla: {self.resources['vanilla']}g")
        print(f"Caramel: {self.resources['caramel']}g")
        print(f"Honey: {self.resources['honey']}g")
        print(f"Cups: {self.resources['cups']}")


    # # This whole thing needs rewritten, it is a mess
    # # Check if there is enough ingredients to make the drink before showing it on the menu!
    # def is_resource_sufficient(self, drink): # There is a bug here when checking none existing drinks
    #     """Returns True when order can be made, False if ingredients are insufficient."""
    #     can_make = True
    #     # for item in menu.name:
    #     #     if menu.ingredients[item] >= self.resources[item]:
    #     #         menu.active = False
    #             # lite the refill indicator and send message to the service
    #     for item in drink.ingredients:
    #         if drink.ingredients[item] > self.resources[item]:
    #             print(f"Sorry there is not enough {item}.")
    #             can_make = False
    #     return can_make
    
    def is_resource_sufficient(self, drink):
        """Returns True when order can be made, False if ingredients are insufficient."""
        can_make = True
        for item in drink.ingredients:
            if drink.ingredients[item] > self.resources[item]:
                print(f"Sorry there is not enough {item}.")
                can_make = False
        return can_make


    def make_coffee(self, order):
        """Deducts the required ingredients from the resources."""
        for item in order.ingredients:
            self.resources[item] -= order.ingredients[item]
        print(f"Here is your {order.name} ☕️. Enjoy!")
        