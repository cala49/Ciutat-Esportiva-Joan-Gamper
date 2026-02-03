from typing import List
from event import Event
from calendary import Calendary

class Restriccion:
    # clase para todas las restricciones
    def validar(self, event: Event, calendary: Calendary) -> tuple[bool, str]:
        # valida si cumple o no la restriccion
        raise NotImplementedError("Las clases deben implementar el método")
    
    def __repr__(self):
        return f"{self.__class__.__name__}"


class RestriccionInclusion(Restriccion):
    # para objetos que requieren de otro para usarse
    def __init__(self, recurso_principal, recurso_requerido):
        
        self.recurso_principal = recurso_principal
        self.recurso_requerido = recurso_requerido
        
    def validar(self, event: Event, calendary: Calendary) -> tuple[bool, str]:       
        # verificar si el evento usa el recurso principal
        if event.use_resource(self.recurso_principal):
            # si usa el recurso requerido
            if not(event.use_resource(self.recurso_requerido)):
                return False, f"❌ Error de Restriccion: Al usar '{self.recurso_principal.name}' también se debe usar '{self.recurso_requerido.name}'"
        
        return True, "✅ Restricción de inclusión cumplida"
    
    def __repr__(self):
        return f"RestriccionInclusion({self.recurso_principal.name} → {self.recurso_requerido.name})"


class RestriccionExclusion(Restriccion):
    # dos objetos no pueden usarse en un mismo evento
    def __init__(self, recurso1, recurso2):
        
        self.recurso1 = recurso1
        self.recurso2 = recurso2
        
    def validar(self, event: Event, calendary: Calendary) -> tuple[bool, str]:
        # dos recursos no esten juntos en un mismo evento A <=> B
        usa_recurso1 = event.use_resource(self.recurso1)
        usa_recurso2 = event.use_resource(self.recurso2)
        
        # A => B
        if usa_recurso1 and not usa_recurso2:
            return False, (
                f"❌ Error de Restriccion: Al usar '{self.recurso1.name}' "
                f"también se debe usar '{self.recurso2.name}'"
        )

        # B => A
        if usa_recurso2 and not usa_recurso1:
            return False, (
                f"❌ Error de Restriccion: '{self.recurso2.name}' "
                f"no puede usarse sin '{self.recurso1.name}'"
        )

        return True, "✅ Restricción de inclusión cumplida"
    
    def __repr__(self):
        return f"RestriccionExclusion({self.recurso1.name} <-> {self.recurso2.name})"


class GestorRestricciones:
    # gestionar las restricciones
    def __init__(self):
        self.restricciones = []
    
    def agregar_restriccion(self, restriccion: Restriccion):
        # agregar restriccion
        self.restricciones.append(restriccion)
    
    def validar_todas(self, event: Event, calendary: Calendary) -> tuple[bool, List[str]]:
        # validar un evento con todas las restricciones
        mensajes = []
        todas_validas = True
        
        for restriccion in self.restricciones:
            valida, mensaje = restriccion.validar(event, calendary)
            mensajes.append(mensaje)
            if not valida:
                todas_validas = False
        
        return todas_validas, mensajes
    
    def limpiar(self):
        # eliminar las restricciones
        self.restricciones.clear()
    
    def listar_restricciones(self) -> List[str]:
        # lista de todas las restricciones
        return [str(r) for r in self.restricciones]