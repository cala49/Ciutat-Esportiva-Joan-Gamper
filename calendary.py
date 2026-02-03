from datetime import datetime, timedelta
from typing import List, Optional
from event import Event

class Calendary: 
    # maneja eventos y conflictos
    def __init__(self):
        # inicializar calendario vacio
        self.events = []  # lista de eventos
        self._last_id = 0  # ID
    
    def generar_id(self) -> int:
        # asignar un id a cada evento
        self._last_id += 1
        return self._last_id
    
    def add_event(self, event: Event, conflicts: bool = True) -> tuple[bool, str]:
        if conflicts:
            conflicto, mensaje = self.veri_conflict(event)
            if conflicto:
                return False, mensaje
        
        # si no hay conflictos
        self.events.append(event)
        return True, f"✅ Evento '{event.name}' agregado."
    
    def delete_event(self, event_id: int) -> tuple[bool, str]:
        # eliminar un evento por el ID
        for i, event in enumerate(self.events):
            if event.id == event_id:
                name = event.name
                del self.events[i]
                return True, f"✅ Evento '{name}' eliminado."
        
        return False, f"❌ No se encontró ningún evento con ID {event_id}."
    
    def find_event(self, event_id: int) -> Optional[Event]:
        # buscar un evento por el ID
        for event in self.events:
            if event.id == event_id:
                return event
        return None
    
    def veri_conflict(self, new_event: Event) -> tuple[bool, str]:
        # verificar si el evento no entra en conflicto con los anteriores
        for current_event in self.events:
            # verificar si se superpone
            if new_event.superposition(current_event):
                # verificar conflictos de recursos
                resources_conflict = []
                for resource in new_event.resources:
                    if current_event.use_resource(resource):
                        resources_conflict.append(resource.name)
                
                if resources_conflict:
                    resources_str = ", ".join(resources_conflict)
                    return True, f"❌ Conflicto: Recursos [{resources_str}] ya están asignados a '{current_event.nombre}' en ese horario."
        
        return False, "✅ No hay conflictos detectados."
    
    def list_events(self, ordenados: bool = True) -> List[Event]:
       # lista de todos los eventos
        if ordenados:
            return sorted(self.events, key=lambda e: e.start)
        return self.events
    
    def eventos_resource(self, recurso_id: int) -> List[Event]:
        # eventos que usan determinado recurso
        return [event for event in self.events if event.use_resource(recurso_id)]
    
    def find_posible_position (self, d_minutes: int, resources_requeried: list, 
                     start_from: datetime, days_to_find: int = 30) -> Optional[tuple[datetime, datetime]]:
        # proximo lugar disponible para un evento
        if start_from is None:
            start_from = datetime.now()

        end_find = start_from + timedelta(days=days_to_find)
        current_hour = start_from
        
        # aproximar la hora
        if current_hour.minute > 0:
            current_hour = current_hour.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        else:
            current_hour = current_hour.replace(second=0, microsecond=0)

        while current_hour < end_find:
            # calcular fin del evento
            end_event = current_hour + timedelta(minutes=d_minutes)
            
            # crear evento temporal para verificar conflicto
            from event import Event
            evento_temp = Event(-1, "Temporal", current_hour, end_event, resources_requeried)

            # verificar conflicto
            conflicto, _ = self.veri_conflict(evento_temp)
            
            if not conflicto:
                # lugar disponible
                return current_hour, end_event
            
            # avanzar al próximo intervalo
            current_hour += timedelta(minutes=30)  # buscar cada 30 minutos

        return None
    
    def to_dict(self) -> dict:
        # convertir a diccionario
        return {
            "last_id": self._last_id,
            "events": [evento.to_dict() for evento in self.events]
        }
        
    def clean(self):
        # elimina los eventos del calendario
        self.events.clear()
        self._last_id = 0