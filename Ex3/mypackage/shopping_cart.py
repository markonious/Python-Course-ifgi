class Shopping_cart:
    # create an empty dic to put items of the cart in it, the key is the item and the value is the quantity
    def __init__(self):
        self.items = {}  

    # a fuction to add items to the cart
    def add(self, item, quantity):
        # it checks if the item already exists in the cart
        if item in self.items:
            self.items[item] += quantity
        # if the item is not there it creates a new entry     
        else:
            self.items[item] = quantity
            
    # a function to remove items from the cart
    def remove(self, item):
        # it checks if the item is already in the cart
        if item in self.items:
            del self.items[item]
            
    # a function to add all items in the cart
    def total(self):
        return sum(self.items.values())
    
    # a function to show all the items in the cart
    def show_items(self):
        for item, qty in self.items.items():
            print(f"{item}: {qty}")

    
            