# main.py
from datetime import datetime, timedelta
from tracemalloc import start
from models import Ball, Kit
from event import Event
from calendary import Calendary

def main():
    print("=== Sistema de Planificación de Ciutat Esportiva Joan Gamper ===\n")
    
    # 1. crear recursos
    balon_futbol = Ball(1, "Balón de Fútbol", "Nike", 5)
    kit_entrenamiento = Kit(2, "Kit de Entrenamiento", "Rojo", 3)
    
    # 2. crear calendario
    calendario = Calendary()
    
    # 3. crear un evento
    start = datetime(2024, 1, 20, 10, 0)
    end = start + timedelta(hours=2)
    evento1 = Event(
        id_event=calendario.generar_id(),
        name="Partido vs Real Sociedad",
        start=start,
        end=end,
        resources=[balon_futbol, kit_entrenamiento]
    )
    
    # 4. intentar agregar el evento
    exito, mensaje = calendario.add_event(evento1)
    print(mensaje)
    
    # 5. listar eventos
    print("\n📅 Eventos en el calendario:")
    for evento in calendario.list_events():
        print(f"  - {evento}")
    
    # 6. buscar un hueco disponible
    print("\n🔍 Buscando hueco para nuevo evento (1.5 horas, mismo balón)...")
    hueco = calendario.find_posible_position(
        d_minutes=90,
        resources_requeried=[balon_futbol],
        start_from=datetime(2024, 1, 20, 12, 0)  # Buscar desde las 12:00 del mismo día
    )
    
    if hueco:
        inicio_hueco, fin_hueco = hueco
        print(f"  ✅ Hueco encontrado: {inicio_hueco.strftime('%d/%m/%Y %H:%M')} a {fin_hueco.strftime('%H:%M')}")
    else:
        print("  ❌ No se encontró hueco disponible en los próximos 30 días.")

if __name__ == "__main__":
    main()