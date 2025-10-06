
class Resource:
    def __init__(self, type: str, index: int, name: str, inStack: int):        
        self.type = type
        self.index = index
        self.name = name       
        self.inStack = inStack        
    def __repr__(self):
        return f"Resource({self.type}, id: {self.index}, {self.name}, {self.inStack} in stack.)"


class Ball(Resource):
    def __init__(self, index: int, name: str, brand: str, inStack: int):
        super().__init__(self, "Sports Equipament", index, name, inStack)  # Llama a los atributos del padre
        self.brand = brand  # Nuevo atributo
           
    def __repr__(self):
       return f"Ball({self.type}, id: {self.index}, {self.name}, {self.brand} brand, {self.inStack} in stack.)"


class Cards(Resource):
    def __init__(self, index: int, name: str, inStack: int):
        super().__init__("Sports Equipament", index, name, inStack)  # Llama a los atributos del padre        
    def __repr__(self):  
        return f"Cards({self.type}, id: {self.index}, {self.name}, {self.inStack} in stack.)"


class Kit(Resource):
    def __init__(self, index: int, name: str, color: str, inStack: int):
        super().__init__("Sports Equipament", index, name, inStack)   # Llama a los atributos del padre   
        self.color = color  # Nuevo atributo     
    def __repr__(self):
        return f"Kit({self.type}, id: {self.index}, {self.name}, {self.color} color, {self.inStack} in stack.)"
