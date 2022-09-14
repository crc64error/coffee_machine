class MenuItem:
    """Models each Menu Item."""
    def __init__(self, name, water, milk, foam, coffee, chocolate, vanilla, caramel, honey, cups, cost):
        self.name = name
        self.cost = cost
        self.ingredients = {
            "water": water,
            "milk": milk,
            "coffee": coffee,
            "chocolate": chocolate,
            "vanilla": vanilla,
            "caramel": caramel,
            "honey": honey,
            "cups": cups
        }


class Menu:
    """Models the Menu with drinks."""
    def __init__(self):
        self.menu = [
            # Other than espresso, all drinks are made to a target of 12oz, or 340ml, coffee is not included in that measurement
            # Vanilla is not included in the 340ml measurement, it is a tiny amount
            # Choclate and Caramel are included in the 340ml measurement, they are a 10ml portions
            MenuItem(name="espresso", water=50, milk=0, foam=0, coffee=36, chocolate=0, vanilla=0, caramel=0, honey=0, cups=1, cost=1.75),
            MenuItem(name="caramel_macchiato", water=100, milk=0, foam=50, coffee=36, chocolate=0, vanilla=0, caramel=10, honey=0, cups=1, cost=2.0),
            MenuItem(name="americano", water=340, milk=0, foam=0, coffee=24, chocolate=0, vanilla=0, caramel=0, honey=0, cups=1, cost=1.5),
            MenuItem(name="vanilla_cappuccino", water=250, milk=90, foam=0, coffee=24, chocolate=0, vanilla=2, caramel=0, honey=0, cups=1, cost=2.5),
            MenuItem(name="caramel_cappuccino", water=245, milk=85, foam=0, coffee=24, chocolate=0, vanilla=0, caramel=10, honey=0, cups=1, cost=2.5),
            MenuItem(name="cortado", water=150, milk=200, foam=0, coffee=24, chocolate=0, vanilla=0, caramel=0, honey=0, cups=1, cost=2.5),
            MenuItem(name="mocha", water=180, milk=160, foam=0, coffee=18, chocolate=0, vanilla=0, caramel=0, honey=0, cups=1, cost=2.5),
            MenuItem(name="chocolate_mocha", water=175, milk=155, foam=0, coffee=18, chocolate=10, vanilla=0, caramel=0, honey=0, cups=1, cost=2.5),
            MenuItem(name="caramel_mocha", water=175, milk=155, foam=0, coffee=18, chocolate=0, vanilla=0, caramel=10, honey=0, cups=1, cost=2.5),
            MenuItem(name="latte", water=200, milk=150, foam=0, coffee=24, chocolate=0, vanilla=0, caramel=0, honey=0, cups=1, cost=2.5),
            MenuItem(name="honey_latte", water=195, milk=145, foam=0, coffee=24, chocolate=0, vanilla=0, caramel=0, honey=10, cups=1, cost=2.5),
            MenuItem(name="vanilla_latte", water=200, milk=150, foam=0, coffee=24, chocolate=0, vanilla=2, caramel=0, honey=0, cups=1, cost=2.5),
        ]

    def get_items(self):
        """Returns all the names of the available menu items"""
        options = ""
        for item in self.menu:
            options += f"{item.name}/"
        return options

    def find_drink(self, order_name):
        """Searches the menu for a particular drink by name. Returns that item if it exists, otherwise returns None"""
        for item in self.menu:
            if item.name == order_name:
                return item
        print("Sorry that item is not available.")
