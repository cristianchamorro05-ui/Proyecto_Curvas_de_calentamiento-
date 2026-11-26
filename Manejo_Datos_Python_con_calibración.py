import serial # Para recibir datos del puerto (enviados por arduino)
import csv # Para gestión de Archivos CSV
import os # Para interactuar con las carpetas del PC
import matplotlib.pyplot as plt # Para realizar gráficas 

# -----------------------------
# CONFIGURACIÓN
# -----------------------------

puerto = "COM4" # Indica el puerto COM donde está conectado Arduino.
baudrate = 9600 # # Indica la velocidad de comunicación entre Arduino y Python, en baudios.

# Carpeta donde se guardarán los datos
carpeta = r"C:\Users\Cristian\OneDrive\Documentos\Experimento_Temperatura"

# Nombre del archivo
nombre_archivo = os.path.join(carpeta, "agua.csv") 

# Crear carpeta si no existe
os.makedirs(carpeta, exist_ok=True)

# -----------------------------
# CONEXIÓN CON ARDUINO
# -----------------------------

arduino = serial.Serial(puerto, baudrate, timeout=1)

print("Conectado a Arduino")
print("Guardando datos y mostrando gráfica...")
print("Cierra la gráfica o presiona Ctrl+C para terminar.")

# -----------------------------
# LISTAS PARA LA GRÁFICA
# -----------------------------

tiempos = []
temperaturas = []

# -----------------------------
# CONFIGURAR GRÁFICA
# -----------------------------

plt.ion()

fig, ax = plt.subplots()

linea, = ax.plot([], [])

ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Temperatura (°C)")
ax.set_title("Curva de calentamiento")

ax.grid(True)

# -----------------------------
# CREAR ARCHIVO CSV
# -----------------------------

with open(nombre_archivo, "w", newline="") as archivo:

    escritor = csv.writer(archivo)
    escritor.writerow(["Tiempo_s", "Temperatura_C"])

    try:
        while True:

            # Leer una línea de Arduino
            linea_serial = arduino.readline().decode("utf-8").strip()
            datos = linea_serial.split(",")

            if len(datos) == 2:
                try:

                    tiempo = float(datos[0])
                    temperatura = float(datos[1])

                except ValueError:
                    continue
                
                # Guardar datos en las listas
                tiempos.append(tiempo)
                temperaturas.append(temperatura)

                # Mostrar en consola
                print(
                    f"Tiempo: {tiempo:.2f} s | "
                    f"Temperatura: {temperatura:.2f} °C"
                )

                # Guardar en CSV
                escritor.writerow([tiempo, temperatura])
                # Actualizar gráfica
                linea.set_xdata(tiempos)
                linea.set_ydata(temperaturas)
                # Ajustar límites automáticamente
                ax.relim()
                ax.autoscale_view()
                # Dibujar
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.pause(0.001)

    except KeyboardInterrupt:
        
        print("\nExperimento terminado.")

# -----------------------------
# CERRAR
# -----------------------------

arduino.close()

plt.ioff()
plt.show()

print(f"Datos guardados en: {nombre_archivo}")