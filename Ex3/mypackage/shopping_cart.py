class Shopping_cart:
    def __init__(self):
        self.items = []
        
    def add(self,item):
        self.items.append(item)
        
    def remove(self,item):
        if item in self.items:
            self.items.remove(item)
    
    def total(self):
        return len(self.items)
    
    
            