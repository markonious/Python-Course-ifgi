import calculator
import shopping_cart
#from mypackage import Shopping_cart

calc = calculator.Calculator()
cart = shopping_cart.Shopping_cart()

print("Addition:", calc.addition(10, 5))
print("Subtraction:", calc.subtraction(10, 5))
print("Multiplication:", calc.multiplication(10, 5))
print("Division:", calc.division(10, 5))

# 1. Add 3 different items
cart.add("Apples", 3)
cart.add("Bananas", 2)
cart.add("Bread", 1)

# 2. Show items and total
print("Cart contents:")
cart.show_items()
print("Total quantity:", cart.total())

# 3. Remove one item
cart.remove("Bananas")

# Show updated cart
print("\nUpdated cart:")
cart.show_items()
print("Total quantity:", cart.total())




