from datetime import datetime

class Event: # def events, name, time and resources
    def __init__(self, id_event: int, name: str, start: datetime, end: datetime, resources: list):
        self.id = id_event
        self.name = name
        self.start = start
        self.end = end
        self.resources = resources # lista de recursos
        
    def __repr__(self):
        # debugging
        resources_str = ", ".join([r.name for r in self.resources])
        return f"Evento(ID:{self.id}, '{self.name}', {self.start.strftime('%Y-%m-%d %H:%M')} -> {self.end.strftime('%Y-%m-%d %H:%M')}, Recursos: [{resources_str}])"

    def __str__(self):
        # representacion de un evento
        return f"{self.name} (ID: {self.id}) - {self.start.strftime('%d/%m/%Y %H:%M')} a {self.end.strftime('%H:%M')}"
    
    def to_dict(self):
        # convirtiendo a diccionario
        return {
            "id": self.id,
            "name": self.name,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "resources_ids": [r.index for r in self.resources]  # Solo guardamos los IDs de los recursos
        }
    def superposition(self, eventOther):
        # verificar si se superponen eventos
        return (self.start < eventOther.end and self.end > eventOther.start)
    
    def use_resource(self, resource): 
        # true si el evento usa el recurso      
        if isinstance(resource, int): 
            # si es un ID
            return any(r.index == resource for r in self.resources)
        else:
            # si es un recurso
            return resource in self.resources 