# creating a class for the  
class Calculator:  
    # a function to add numbers
    def addition(self,a,b):
        return a+b
    
    # a function to subtract numbers
    def subtraction(self,a,b):
        return a-b
    
    # a function to multiply numbers
    def multiplication(self,a,b):
        return a*b
    
    # a function to divide numbers
    def division(self,a,b):
        if b == 0:
            return "please enter a valid number"
        return a/b

 
