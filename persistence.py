# persistence.py
import json
from datetime import datetime
from typing import Dict, List, Any
from models import Resource, Ball, Cards, Kit, Supplements
from event import Event
from calendary import Calendary

class GestorPersistencia:
    # guardado de datos del sistema
    def __init__(self, archivo_datos: str = "datos.json"):
        self.archivo_datos = archivo_datos
        self.diccionario_recursos = {}  # para mapear IDs a resource
    
    def _crear_recurso_desde_dict(self, datos: Dict) -> Resource:
        # crea un objeto resource a partir de un diccionario
        tipo_recurso = datos.get("subtype", "").lower()
        
        if tipo_recurso == "ball":
            return Ball(
                index=datos["index"],
                name=datos["name"],
                brand=datos.get("brand", ""),
                inStack=datos["inStack"]
            )
        elif tipo_recurso == "cards":
            return Cards(
                index=datos["index"],
                name=datos["name"],
                inStack=datos["inStack"]
            )
        elif tipo_recurso == "kit":
            return Kit(
                index=datos["index"],
                name=datos["name"],
                color=datos.get("color", ""),
                inStack=datos["inStack"]
            )
        elif tipo_recurso == "supplements":
            return Supplements(
                index=datos["index"],
                name=datos["name"],
                inStack=datos["inStack"]
            )
        else:
            # Recurso genérico
            return Resource(
                type=datos.get("type", "Sports Equipment"),
                index=datos["index"],
                name=datos["name"],
                inStack=datos["inStack"]
            )
    
    def cargar_datos(self) -> tuple[List[Resource], Calendary]:
        try:
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                datos = json.load(f)
        except FileNotFoundError:
            print("⚠️ Archivo no encontrado. Se creará uno nuevo al guardar.")
            return [], Calendary()
        except json.JSONDecodeError:
            print("❌ El archivo JSON está corrupto.")
            return [], Calendary()

        # Cargar recursos y crear diccionario ID -> Objeto
        recursos = []
        recursos_por_id = {}
        for recurso_data in datos.get("recursos", []):
            try:
                recurso = self._crear_recurso_desde_dict(recurso_data)
                recursos.append(recurso)
                recursos_por_id[recurso.index] = recurso
            except Exception as e:
                print(f"⚠️ Error al cargar recurso {recurso_data.get('index')}: {e}")

        # Cargar eventos
        calendario = Calendary()
        calendario._last_id = datos.get("calendario", {}).get("last_id", 0)
    
        for evento_data in datos.get("calendario", {}).get("events", []):
            try:
                evento = Event.from_dict(evento_data, recursos_por_id)
                calendario.events.append(evento)
            except Exception as e:
                print(f"❌ Error al cargar evento {evento_data.get('id', '?')}: {e}")

        print(f"✅ Datos cargados: {len(recursos)} recursos, {len(calendario.events)} eventos")
        return recursos, calendario
    
    def guardar_datos(self, recursos: List[Resource], calendario: Calendary) -> bool:
        # guarda los datos en un archivo JSON
        datos = {
            "recursos": [r.to_dict() for r in recursos],
            "calendario": calendario.to_dict(),
            "fecha_guardado": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        try:
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2, ensure_ascii=False)
            print(f"✅ Datos guardados en {self.archivo_datos}")
            return True
        except Exception as e:
            print(f"❌ Error al guardar datos: {e}")
            return False
    
    def crear_datos_ejemplo(self):
        # crear archivo de ejemplo con los datos iniciales
        recursos = [
            Ball(1, "Balón de Fútbol 1", "Nike", 5),
            Ball(2, "Balón de Fútbol 2", "Adidas", 3),
            Kit(3, "Kit de Entrenamiento", "Rojo", 2),
            Cards(4, "Amarillas", 10),
            Cards(5, "Rojas", 5),
            Supplements(6, "Espinilleras", 8),
            Supplements(7, "Bebida Energética", 15)
        ]
        
        calendario = Calendary()
        
        evento1 = Event(
            id_event=calendario.generar_id(),
            name="Entrenamiento de Fútbol",
            start=datetime(2024, 1, 20, 10, 0),
            end=datetime(2024, 1, 20, 12, 0),
            resources=[recursos[0], recursos[2]]
        )
        calendario.add_event(evento1, conflicts=False)
        
        evento2 = Event(
            id_event=calendario.generar_id(),
            name="Partido vs Real Madrid Castilla",
            start=datetime(2024, 1, 21, 18, 0),
            end=datetime(2024, 1, 21, 22, 0),
            resources=[recursos[1], recursos[3], recursos[4]]
        )
        calendario.add_event(evento2, conflicts=False)
        
        self.guardar_datos(recursos, calendario)
        print("📁 Archivo creado exitosamente.")