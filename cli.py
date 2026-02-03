import json
import sys
from datetime import datetime, timedelta
from models import Resource, Ball, Kit, Cards, Supplements
from event import Event
from calendary import Calendary
from contranins import RestriccionInclusion, RestriccionExclusion, GestorRestricciones
from persistence import GestorPersistencia

class InterfazConsola:
    # interfaz para linea de comandos 
    def __init__(self):
        self.gestor_persistencia = GestorPersistencia()
        self.gestor_restricciones = GestorRestricciones()
        self.recursos = []
        self.calendario = None
        self.c_datos()
        
    def c_datos(self):
        # crear datos al iniciar
        print("🔃 Cargando datos del sistema...")
        self.recursos, self.calendario = self.gestor_persistencia.cargar_datos()

        # si no hay datos, crear ejemplo
        if not self.recursos and not self.calendario.events:
            print("📁 No se encontraron datos. Creando ejemplo...")
            self.gestor_persistencia.crear_datos_ejemplo()
            self.recursos, self.calendario = self.gestor_persistencia.cargar_datos()
    
    def guardar_datos(self):
    # guarda datos en JSON
        if self.calendario is None or not self.recursos:
            print("⚠️ No hay datos para guardar.")
            return
    
    # guardar datos usando GestorPersistencia
        exito = self.gestor_persistencia.guardar_datos(self.recursos, self.calendario)
        if exito:
            print("✅ Datos guardados correctamente.")
        else:
            print("❌ Error al guardar los datos.")

       
       
    def mostrar_menu_principal(self):
        # menu
        while True:
            print("\n" + "="*50)
            print("🎯 PLANIFICADOR INTELIGENTE DEL FÚTBOL CLUB BARCELONA")
            print("="*50)
            print("1. 📅 Ver todos los eventos")
            print("2. ➕ Agregar nuevo evento")
            print("3. ❌ Eliminar evento")
            print("4. 🔍 Buscar hueco disponible")
            print("5. 📋 Listar recursos disponibles")
            print("6. ⚙️ Gestionar restricciones")
            print("7. 📥 Cargar datos")
            print("8. 💾 Guardar datos")
            print("9. 📤 Crear datos de ejemplo")
            print("10. 🚪 Salir")
            print("="*50)
            
            opcion = input("Seleccione una opción (1-10): ").strip()
            
            if opcion == "1":
                self.listar_eventos()
            elif opcion == "2":
                self.agregar_evento()
            elif opcion == "3":
                self.eliminar_evento()
            elif opcion == "4":
                self.buscar_hueco()
            elif opcion == "5":
                self.listar_recursos()
            elif opcion == "6":
                self.menu_restricciones()
            elif opcion == "7":
                self.cargar_datos()
            elif opcion == "8":
                self.guardar_datos()
            elif opcion == "9":
                self.crear_datos_ejemplo()
            elif opcion == "10":
                print("👋 ¡Hasta luego!")
                self.guardar_datos()  # guardar antes de salir
                sys.exit(0)
            
            else:
                print("❌ Opción no válida. Intente de nuevo.")
    
    def listar_eventos(self):
        # listar los eventos en el calendario
        
        if self.calendario is None:
            raise ValueError("Calendario no inicializado")
        
        eventos = self.calendario.list_events()
        
        if not eventos:
            print("\n📭 No hay eventos programados.")
            return
        
        print(f"\n📅 EVENTOS PROGRAMADOS ({len(eventos)}):")
        print("-" * 60)
        
        for i, evento in enumerate(eventos, 1):
            print(f"{i}. {evento}")
            print(f"   Recursos: {', '.join([r.name for r in evento.resources])}")
            print(f"   Duración: {(evento.end - evento.start).seconds // 3600} horas")
            print("-" * 60)
    
    def agregar_evento(self):
        # agregar un evento interactivo
        print("\n➕ AGREGAR NUEVO EVENTO")
        print("-" * 40)
        
        # 1. nombre
        nombre = input("Nombre del evento: ").strip()
        if not nombre:
            print("❌ El nombre es obligatorio.")
            return
        
        # 2. fecha y hora
        try:
            fecha_str = input("Fecha (YYYY-MM-DD): ").strip()
            hora_inicio_str = input("Hora de inicio (HH:MM): ").strip()
            duracion_str = input("Duración en minutos: ").strip()
            
            # parsear fechas
            inicio = datetime.strptime(f"{fecha_str} {hora_inicio_str}", "%Y-%m-%d %H:%M")
            duracion = int(duracion_str)
            fin = inicio + timedelta(minutes=duracion)
            
            # verificar que no sea en el pasado
            if inicio < datetime.now():
                print("❌ No se pueden crear eventos en el pasado.")
                return
                
        except ValueError:
            print("❌ Formato de fecha/hora inválido.")
            return
        
        # 3. seleccionar recursos
        print("\n📋 RECURSOS DISPONIBLES:")
        for i, recurso in enumerate(self.recursos, 1):
            print(f"{i}. {recurso}")
        
        seleccion = input("\nSeleccione recursos (separados por coma, ej: 1,3): ").strip()
        
        if not seleccion:
            print("❌ Debe seleccionar al menos un recurso.")
            return
        
        try:
            indices = [int(idx.strip()) - 1 for idx in seleccion.split(",")]
            recursos_seleccionados = [self.recursos[idx] for idx in indices if 0 <= idx < len(self.recursos)]
            
            if not recursos_seleccionados:
                print("❌ No se seleccionaron recursos válidos.")
                return
                
        except (ValueError, IndexError):
            print("❌ Selección inválida.")
            return
        
        # 4. crear evento
        
        if self.calendario is None:
            raise ValueError("Calendario no inicializado")
        
        evento = Event(
            id_event=self.calendario.generar_id(),
            name=nombre,
            start=inicio,
            end=fin,
            resources=recursos_seleccionados
        )
        
        # 5. verificar conflicto
        conflicto, mensaje_conflicto = self.calendario.veri_conflict(evento)
        if conflicto:
            print(f"\n{mensaje_conflicto}")
            return
        
        # 6. verificar restricciones
        validas, mensajes_restricciones = self.gestor_restricciones.validar_todas(evento, self.calendario)
        if not validas:
            print("\n❌ RESTRICCIONES VIOLADAS:")
            for mensaje in mensajes_restricciones:
                if "❌" in mensaje:
                    print(f"  {mensaje}")
            return
        
        # 7. agregar evento
        exito, mensaje = self.calendario.add_event(evento, conflicts=False)
        print(f"\n{mensaje}")
        
        # mostrar resumen
        if exito:
            print(f"\n📋 RESUMEN DEL EVENTO:")
            print(f"  Nombre: {nombre}")
            print(f"  Fecha: {inicio.strftime('%d/%m/%Y')}")
            print(f"  Hora: {inicio.strftime('%H:%M')} - {fin.strftime('%H:%M')}")
            print(f"  Recursos: {', '.join([r.name for r in recursos_seleccionados])}")
    
    def eliminar_evento(self):
        
        if self.calendario is None:
            raise ValueError("Calendario no inicializado")
        
        # eliminar evento existente
        eventos = self.calendario.list_events()
        
        if not eventos:
            print("\n📭 No hay eventos para eliminar.")
            return
        
        print("\n❌ ELIMINAR EVENTO")
        print("-" * 40)
        
        for i, evento in enumerate(eventos, 1):
            print(f"{i}. {evento.name} (ID: {evento.id}) - {evento.start.strftime('%d/%m/%Y %H:%M')}")
        
        try:
            seleccion = int(input("\nSeleccione evento a eliminar (número): ").strip()) - 1
            if 0 <= seleccion < len(eventos):
                evento_a_eliminar = eventos[seleccion]
                exito, mensaje = self.calendario.delete_event(evento_a_eliminar.id)
                print(f"\n{mensaje}")
            else:
                print("❌ Selección inválida.")
        except ValueError:
            print("❌ Entrada inválida.")
    
    def buscar_hueco(self):
        # buscar espacio para evento disponible
        print("\n🔍 BUSCAR HUECO DISPONIBLE")
        print("-" * 40)
        
        # 1. duración
        try:
            duracion = int(input("Duración del evento (minutos): ").strip())
            if duracion <= 0:
                print("❌ Duración debe ser positiva.")
                return
        except ValueError:
            print("❌ Duración inválida.")
            return
        
        # 2. seleccionar recursos
        print("\n📋 RECURSOS NECESARIOS:")
        for i, recurso in enumerate(self.recursos, 1):
            print(f"{i}. {recurso}")
        
        seleccion = input("\nSeleccione recursos (separados por coma): ").strip()
        
        if not seleccion:
            print("❌ Debe seleccionar al menos un recurso.")
            return
        
        try:
            indices = [int(idx.strip()) - 1 for idx in seleccion.split(",")]
            recursos_necesarios = [self.recursos[idx] for idx in indices if 0 <= idx < len(self.recursos)]
            
            if not recursos_necesarios:
                print("❌ No se seleccionaron recursos válidos.")
                return
                
        except (ValueError, IndexError):
            print("❌ Selección inválida.")
            return
        
        # 3. buscar hueco
        print("\n🔎 Buscando hueco disponible...")
        
        if self.calendario is None:
            raise ValueError("Calendario no inicializado")
        
        hueco = self.calendario.find_posible_position(
            d_minutes=duracion,
            resources_requeried=recursos_necesarios,
            start_from=datetime.now()
        )
        
        if hueco:
            inicio, fin = hueco
            print(f"\n✅ HUECO ENCONTRADO:")
            print(f"  Fecha: {inicio.strftime('%A, %d de %B de %Y')}")
            print(f"  Hora: {inicio.strftime('%H:%M')} - {fin.strftime('%H:%M')}")
            print(f"  Recursos disponibles: {', '.join([r.name for r in recursos_necesarios])}")
            
            # preguntar si quiere crear evento
            crear = input("\n¿Crear evento en este hueco? (s/n): ").strip().lower()
            if crear == 's':
                nombre = input("Nombre del evento: ").strip()
                if nombre:
                    evento = Event(
                        id_event=self.calendario.generar_id(),
                        name=nombre,
                        start=inicio,
                        end=fin,
                        resources=recursos_necesarios
                    )
                    exito, mensaje = self.calendario.add_event(evento)
                    print(f"\n{mensaje}")
        else:
            print("\n❌ No se encontró hueco disponible en los próximos 30 días.")
    
    def listar_recursos(self):
        # todos los recursos disponibles
        print(f"\n📋 RECURSOS DISPONIBLES ({len(self.recursos)}):")
        print("-" * 60)
        
        for i, recurso in enumerate(self.recursos, 1):
            print(f"{i}. {recurso}")
        
        # estadísticas
        print("\n📊 ESTADÍSTICAS:")
        print(f"  Total de recursos: {len(self.recursos)}")
        
        # por tipo
        tipos = {}
        for recurso in self.recursos:
            tipo = recurso.__class__.__name__
            tipos[tipo] = tipos.get(tipo, 0) + 1
        
        for tipo, cantidad in tipos.items():
            print(f"  {tipo}: {cantidad}")
    
    def menu_restricciones(self):
        # gestion de restricciones
        while True:
            print("\n" + "="*40)
            print("⚙️  GESTIÓN DE RESTRICCIONES")
            print("="*40)
            print("1. 📋 Ver restricciones actuales")
            print("2. ➕ Agregar restricción de inclusión")
            print("3. ➖ Agregar restricción de exclusión")
            print("4. 🗑️  Limpiar todas las restricciones")
            print("5. ↩️  Volver al menú principal")
            print("="*40)
            
            opcion = input("Seleccione una opción (1-5): ").strip()
            
            if opcion == "1":
                self.listar_restricciones()
            elif opcion == "2":
                self.agregar_restriccion_inclusion()
            elif opcion == "3":
                self.agregar_restriccion_exclusion()
            elif opcion == "4":
                self.limpiar_restricciones()
            elif opcion == "5":
                break
            else:
                print("❌ Opción no válida.")
    
    def listar_restricciones(self):
        # lista de todas las restricciones
        restricciones = self.gestor_restricciones.listar_restricciones()
        
        if not restricciones:
            print("\n📭 No hay restricciones configuradas.")
            return
        
        print(f"\n📋 RESTRICCIONES CONFIGURADAS ({len(restricciones)}):")
        print("-" * 60)
        
        for i, restriccion in enumerate(restricciones, 1):
            print(f"{i}. {restriccion}")
    
    def agregar_restriccion_inclusion(self):
        # agregar restriccion
        print("\n➕ AGREGAR RESTRICCIÓN DE INCLUSIÓN")
        print("(Si se usa el recurso A, también se debe usar el recurso B)")
        print("-" * 50)
        
        # listar recursos
        self.listar_recursos()
        
        try:
            idx_a = int(input("\nÍndice del recurso principal (A): ").strip()) - 1
            idx_b = int(input("Índice del recurso requerido (B): ").strip()) - 1
            
            if 0 <= idx_a < len(self.recursos) and 0 <= idx_b < len(self.recursos):
                recurso_a = self.recursos[idx_a]
                recurso_b = self.recursos[idx_b]
                
                restriccion = RestriccionInclusion(recurso_a, recurso_b)
                self.gestor_restricciones.agregar_restriccion(restriccion)
                
                print(f"\n✅ Restricción agregada: {restriccion}")
            else:
                print("❌ Índices inválidos.")
        except ValueError:
            print("❌ Entrada inválida.")
    
    def agregar_restriccion_exclusion(self):
        # agregar restriccion de no poder usar 2 a la vez
        print("\n➖ AGREGAR RESTRICCIÓN DE EXCLUSIÓN")
        print("(El recurso A y el recurso B no pueden usarse juntos)")
        print("-" * 50)
        
        # listar recursos
        self.listar_recursos()
        
        try:
            idx_a = int(input("\nÍndice del primer recurso (A): ").strip()) - 1
            idx_b = int(input("Índice del segundo recurso (B): ").strip()) - 1
            
            if 0 <= idx_a < len(self.recursos) and 0 <= idx_b < len(self.recursos):
                recurso_a = self.recursos[idx_a]
                recurso_b = self.recursos[idx_b]
                
                restriccion = RestriccionExclusion(recurso_a, recurso_b)
                self.gestor_restricciones.agregar_restriccion(restriccion)
                
                print(f"\n✅ Restricción agregada: {restriccion}")
            else:
                print("❌ Índices inválidos.")
        except ValueError:
            print("❌ Entrada inválida.")
    
    def limpiar_restricciones(self):
        # eliminar las restricciones
        confirmacion = input("\n⚠️ ¿Está seguro de eliminar TODAS las restricciones? (s/n): ").strip().lower()
        if confirmacion == 's':
            self.gestor_restricciones.limpiar()
            print("✅ Todas las restricciones han sido eliminadas.")
    
    def crear_datos_ejemplo(self):
        print("📤 Creando datos de ejemplo...")
        self.gestor_persistencia.crear_datos_ejemplo()
        print("✅ Datos de ejemplo creados")
        
    def cargar_datos(self):
        # cargar los datos en JSON
        print("🔃 Cargando datos del sistema...")
        self.recursos, self.calendario = self.gestor_persistencia.cargar_datos()
    
        if not self.recursos and not self.calendario.events:
            print("📁 No se encontraron datos. Creando ejemplo...")
            self.gestor_persistencia.crear_datos_ejemplo()
            self.recursos, self.calendario = self.gestor_persistencia.cargar_datos()
    
        print(f"✅ Datos cargados: {len(self.recursos)} recursos, {len(self.calendario.events)} eventos")

def main():
    # funcion principal para la app
    try:
        app = InterfazConsola()
        app.mostrar_menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Aplicación interrumpida por el usuario.")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()