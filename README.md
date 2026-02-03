# Planificador Inteligente del Futbol Club Barcelona

## Descripción
Sistema de planificación para la Cuitat Esportiva Joan Gamper que gestiona eventos, equipamiento y recursos con restricciones.

## Eventos
Actividades deportivas que requieren equipamiento:
- Entrenamientos
- Partidos
- Eventos especiales

## Recursos
Equipamiento deportivo disponible:
- Balones 
- Kits de entrenamiento
- Tarjetas
- Suplementos deportivos

## Restricciones Implementadas

### 1. Restricción de Inclusión (Co-requisito)
- Si se usa un "Tarjeta Amarilla", también se debe usar "Tarjeta Roja"
- Los suplementos energéticos requieren supervisión del kit médico

### 2. Restricción de Exclusión (Mutua)
- No se pueden usar 2 Balones al mismo tiempo
- Cualquier otra restriccion que se le pueda ocurrir al usuario

## Acerca de Ciutat Esportiva Joan Gamper 
En principio, como todo fanático del FC Barcelona, me impulsó la idea de crear un sistema inteligente de gestion de fútbol, la preparacion de partidos, entrenamientos, en fin, todo lo que se le pueda ocurrir al usuario mientras que use parte del equipamiento que brinda esta gran instalación. Se implementó una interfaz visual para la consola bastante cómoda para quien tenga el placer de disfrutar de este gestionador de eventos. Espero que disfrute al máximo de esta aplicación ya que exhorta a la creatividad e impone reglas a seguir para hacer de su experiencia lo más realista posible. Fue un reto interesante, al menos para su desarrollador, ya que no se suele mezclar el deporte con la computación, sin embargo los cuervos de MATCOM fuimos "bronce" en el Torneo Universitario de Futbol "Juegos Caribes" desmintiendo esta creencia popular.

## No fue tarea fácil
Desde el inicio solo habia una idea clara, utilizar POO para el desarrollo de la apk, esto permitió el encapsulamiento y etendimiento del codigo para una posterior mejora, el "crear tipos de datos" facilitó mucho el trabajo en el tema de la comparación, en sí, lo que más dificultó este proyecto fue la implementación de un sistema de guardado y cargado ya que se habia inicializado todo al ejecutar el programa y entonces cuando se cargaba un archivo .JSON, el programa se reiniciaba por la incialización dentro de la clase "Interfaz Consola". 

## Requisitos
- Python 3.8 o superior