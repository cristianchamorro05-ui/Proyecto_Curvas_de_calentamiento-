#include <OneWire.h>             // Incluye la librería necesaria para la comunicación OneWire.
#include <DallasTemperature.h>   // Incluye la librería para controlar sensores de temperatura.

#define pinDatos 2               // Define el pin digital 2 de Arduino como el pin de datos del sensor.

OneWire oneWire(pinDatos);            // Crea el objeto de comunicación OneWire usando el pin definido anteriormente.
DallasTemperature sensores(&oneWire); // Crea el objeto que permite controlar el sensor de temperatura.

unsigned long tiempoInicio;           // Variable que almacenará el instante en que comienza el experimento. 
unsigned long tiempoAnterior = 0;     // Almacena el tiempo de la última medición realizada.
const unsigned long intervalo = 1000; // Define un intervalo de medición de 1000 ms (1 segundo).

void setup() {                    // Función que se ejecuta una sola vez al iniciar Arduino.
  Serial.begin(9600);             // Inicia la comunicación serial a una velocidad de 9600 baudios.
  sensores.begin();               // Inicializa el sensor de temperatura.

  tiempoInicio = millis();        // Guarda el tiempo inicial del experimento en milisegundos.
  Serial.println("");             // Imprime una línea vacía en el monitor serial.
  Serial.println("tiempo_s,temperatura_C"); // Imprime los encabezados de las columnas para el archivo CSV.
}

void loop() {                     // Función que se ejecuta continuamente mientras el Arduino está encendido.
  unsigned long ahora = millis(); // Obtiene el tiempo actual desde que Arduino comenzó a funcionar.

  if (ahora - tiempoAnterior >= intervalo) { // Comprueba si ha transcurrido el intervalo establecido.
    tiempoAnterior = ahora;                  // Actualiza el instante correspondiente a la última medición.

    float segundos = (ahora - tiempoInicio) / 1000.0; // Convierte el tiempo transcurrido de milisegundos a segundos.

    sensores.requestTemperatures();           // Solicita al sensor que realice una nueva medición de temperatura.
    float temp = sensores.getTempCByIndex(0); // Obtiene la temperatura en °C del primer sensor conectado.

    Serial.print(segundos);        // Envía el tiempo transcurrido al puerto serial.
    Serial.print(",");             // Imprime una coma para separar las columnas del archivo CSV.
    Serial.println(temp);          // Envía la temperatura y termina la línea de datos.
  }
}