
class Resource:
    def __init__(self, type: str, index: int, name: str, inStack: int):        
        self.type = type
        self.index = index
        self.name = name       
        self.inStack = inStack        
    
    def __repr__(self):
        return f"Resource({self.type}, id: {self.index}, {self.name}, {self.inStack} in stack.)"
    
    def __eq__(self, other):
        # comparar recursos por su ID
        if isinstance(other, Resource):
            return self.index == other.index
        return False
    
    def to_dict(self):
        # convertir a diccionario 
        return {
            "type": self.type,
            "index": self.index,
            "name": self.name,
            "inStack": self.inStack
        }
    
        


class Ball(Resource):
    def __init__(self, index: int, name: str, brand: str, inStack: int):
        super().__init__("Sports Equipment", index, name, inStack)
        self.brand = brand
           
    def __repr__(self):
        return f"Ball({self.type}, id: {self.index}, {self.name}, {self.brand} brand, {self.inStack} in stack.)"
    
    def to_dict(self):
        dict_resource = super().to_dict()
        dict_resource["brand"] = self.brand
        dict_resource["subtype"] = "Ball"
        return dict_resource


class Cards(Resource):
    def __init__(self, index: int, name: str, inStack: int):
        super().__init__("Sports Equipment", index, name, inStack)
    
    def __repr__(self):
        return f"Cards({self.type}, id: {self.index}, {self.name}, {self.inStack} in stack.)"
    
    def to_dict(self):
        dict_resource = super().to_dict()
        dict_resource["subtype"] = "Cards"
        return dict_resource


class Kit(Resource):
    def __init__(self, index: int, name: str, color: str, inStack: int):
        super().__init__("Sports Equipment", index, name, inStack)
        self.color = color
    
    def __repr__(self):
        return f"Kit({self.type}, id: {self.index}, {self.name}, {self.color} color, {self.inStack} in stack.)"
    
    def to_dict(self):
        dict_resource = super().to_dict()
        dict_resource["color"] = self.color
        dict_resource["subtype"] = "Kit"
        return dict_resource


class Supplements(Resource):
    def __init__(self, index: int, name: str, inStack: int):
        super().__init__("Sports Equipment", index, name, inStack)
    
    def __repr__(self):
        return f"Supplements({self.type}, id: {self.index}, {self.name}, {self.inStack} in stack.)"
    
    def to_dict(self):
        dict_recurso = super().to_dict()
        dict_recurso["subtype"] = "Supplements"
        return dict_recurso