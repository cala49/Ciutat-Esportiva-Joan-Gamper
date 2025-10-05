class Resource:
    def __init__(self, name, inStack = 0):        
        self.name = name
        self.inStack = inStack        
    def __repr__(self):
        return f"Resource({self.name}, {self.inStack} in stack.)"


class Ball(Resource):
    def __init__(self, name, brand, inStack=0):
        super().__init__(name, inStack)  # Llama a los atributos del padre
        self.brand = brand  # Nuevo atributo
           
    def __repr__(self):
       return f"Ball({self.name}, {self.brand} brand, {self.inStack} in stack.)"


class Cards(Resource):
    def __init__(self, name, inStack=0):
        super().__init__(name, inStack)  # Llama a los atributos del padre
    def __repr__(self):
        return f"Cards({self.name}, {self.inStack} in stack.)"

Mercury = Ball("Mercury", "Adidas", 5)
print(Mercury)

yellow = Cards("Yellow", 2)
print(yellow)
