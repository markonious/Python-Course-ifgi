# importing our modules
import calculator
import shopping_cart

# creating an object from calculator class
calc = calculator.Calculator()

# creating an object from shopping cart class
cart = shopping_cart.Shopping_cart()


print("Addition:", calc.addition(10, 5))
print("Subtraction:", calc.subtraction(10, 5))
print("Multiplication:", calc.multiplication(10, 5))
print("Division:", calc.division(10, 5))

# Adding different items to the cart
cart.add("Apples", 3)
cart.add("Bananas", 2)
cart.add("Bread", 1)

# Show items and total
print("Cart contents:")
cart.show_items()
print("Total quantity:", cart.total())

# Remove one item
cart.remove("Bananas")

# Show updated cart
print("\nUpdated cart:")
cart.show_items()
print("Total quantity:", cart.total())




