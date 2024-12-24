import pyaudio
import wave
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import json
import os

# --- 1. Función para grabar audio ---
def record_audio(filename, duration, sample_rate=44100, channels=1, chunk_size=1024):
    """Graba audio y guarda en un archivo WAV."""
    audio_format = pyaudio.paInt16  # Formato de audio: 16 bits por muestra
    pa = pyaudio.PyAudio()

    # Configurar el stream
    stream = pa.open(format=audio_format, channels=channels, rate=sample_rate, input=True, frames_per_buffer=chunk_size)

    print("Grabando...")
    frames = []

    # Grabar audio por la duración especificada
    for _ in range(0, int(sample_rate / chunk_size * duration)):
        data = stream.read(chunk_size)
        frames.append(data)

    print("Grabación finalizada.")

    # Finalizar el stream
    stream.stop_stream()
    stream.close()
    pa.terminate()

    # Guardar en archivo WAV
    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(pa.get_sample_size(audio_format))
        wf.setframerate(sample_rate)
        wf.writeframes(b''.join(frames))

    print(f"Archivo guardado como {filename}")

# --- 2. Función para cargar audio ---
def load_audio(file):
    """Carga un archivo WAV y devuelve la frecuencia de muestreo y los datos."""
    sample_rate, data = wavfile.read(file)
    if data.ndim > 1:  # Convertir a mono si es estéreo
        data = data[:, 0]
    return sample_rate, data

# --- 3. Función para calcular la FFT ---
def compute_fft(data, sample_rate):
    """Calcula el espectro de frecuencias usando la FFT."""
    N = len(data)
    fft = np.fft.fft(data)
    freqs = np.fft.fftfreq(N, d=1/sample_rate)
    magnitude = np.abs(fft)
    positive_freqs = freqs[:N // 2]
    positive_magnitude = magnitude[:N // 2]
    return positive_freqs, positive_magnitude

# --- 4. Función para encontrar la frecuencia fundamental ---
def find_fundamental_frequency(freqs, magnitude):
    """Encuentra la frecuencia fundamental en el espectro."""
    index = np.argmax(magnitude)
    return freqs[index]

# --- 5. Guardar frecuencia fundamental en un archivo ---
def save_frequency_to_file(name, frequency, file="frequencies.json"):
    """Guarda la frecuencia fundamental con un nombre en un archivo JSON."""
    if not os.path.exists(file):
        # Crear archivo vacío si no existe
        with open(file, "w") as f:
            json.dump([], f)

    with open(file, "r") as f:
        data = json.load(f)  # Cargar datos existentes

    # Añadir nueva grabación con nombre y frecuencia
    data.append({"nombre": name, "frecuencia": frequency})

    with open(file, "w") as f:
        json.dump(data, f, indent=4)

    print(f"Frecuencia guardada: {frequency:.2f} Hz con el nombre '{name}'.")

def display_saved_frequencies(file="frequencies.json"):
    """Lee y muestra todas las frecuencias guardadas en el archivo."""
    if not os.path.exists(file):
        print("No hay frecuencias guardadas todavía.")
        return

    with open(file, "r") as f:
        data = json.load(f)

    print("Frecuencias guardadas:")
    for i, entry in enumerate(data, start=1):
        print(f"{i}. {entry['nombre']} - {entry['frecuencia']} Hz")

# --- Menú Principal ---
if __name__ == "__main__":
    file = "nota.wav"  # Nombre predeterminado del archivo de audio
    while True:
        print("\nMenú Principal")
        print("1. Grabar Audio")
        print("2. Visualizar Gráfico del Espectro")
        print("3. Mostrar Todas las Frecuencias Guardadas")
        print("4. Salir")
        choice = input("Seleccione una opción: ")

        if choice == "1":
            name = input("Ingrese un nombre para la grabación: ")
            duration = int(input("Ingrese la duración de la grabación (en segundos): "))
            record_audio(file, duration=duration)

            # Analizar y guardar frecuencia fundamental
            sample_rate, data = load_audio(file)
            freqs, magnitude = compute_fft(data, sample_rate)
            fundamental_freq = find_fundamental_frequency(freqs, magnitude)
            save_frequency_to_file(name, fundamental_freq)

        elif choice == "2":
            try:
                sample_rate, data = load_audio(file)
                freqs, magnitude = compute_fft(data, sample_rate)
                fundamental_freq = find_fundamental_frequency(freqs, magnitude)

                print(f"\nFrecuencia Fundamental: {fundamental_freq:.2f} Hz")

                # Graficar el espectro
                plt.figure(figsize=(10, 5))
                plt.plot(freqs, magnitude, label="Espectro de Frecuencias")
                plt.axvline(fundamental_freq, color='r', linestyle='--', label=f"Frecuencia Fundamental: {fundamental_freq:.2f} Hz")
                plt.title("Espectro de Frecuencias")
                plt.xlabel("Frecuencia (Hz)")
                plt.ylabel("Magnitud")
                plt.legend()
                plt.grid()
                plt.show()

            except FileNotFoundError:
                print("Error: No se ha encontrado el archivo de audio. Grabe uno primero.")

        elif choice == "3":
            display_saved_frequencies()

        elif choice == "4":
            print("Saliendo del programa.")
            break

        else:
            print("Opción inválida. Intente nuevamente.")
