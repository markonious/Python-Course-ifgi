# creating a class for the 
class Calculator:

    def addition(self,a,b):
        return a+b

    def subtraction(self,a,b):
        return a-b

    def multiplication(self,a,b):
        return a*b

    def division(self,a,b):
        if b == 0:
            return "please enter a valid number"
        return a/b

 
