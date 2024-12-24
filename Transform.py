from Table_frec import EQUIVALENCIAS
import json

# QuickSort con el cuarto elemento como pivote
def quicksort(arr):
    """Ordena una lista usando QuickSort con el cuarto elemento como pivote."""
    if len(arr) <= 1:  # Caso base
        return arr
    pivot_index = min(3, len(arr) - 1)  # El cuarto elemento o el último si hay menos
    pivot = arr[pivot_index]
    less_than_pivot = [x for x in arr if x < pivot]  # Elementos menores al pivote
    greater_than_pivot = [x for x in arr if x > pivot]  # Elementos mayores al pivote
    return quicksort(less_than_pivot) + [pivot] + quicksort(greater_than_pivot)  # Combinar todo

# Función para encontrar la nota más cercana
def get_closest_note(frequency):
    """Devuelve la nota más cercana a una frecuencia dada."""
    closest_freq = min(EQUIVALENCIAS.keys(), key=lambda x: abs(x - frequency))
    return EQUIVALENCIAS[closest_freq], closest_freq

# Función para determinar el rango de una frecuencia
def get_note_range(frequency):
    """Devuelve el rango de notas entre el cual se encuentra la frecuencia."""
    freqs = list(EQUIVALENCIAS.keys())
    sorted_freqs = quicksort(freqs)  # Ordenar frecuencias usando QuickSort

    # Buscar el rango en el que se encuentra la frecuencia
    for i in range(len(sorted_freqs) - 1):
        if sorted_freqs[i] <= frequency < sorted_freqs[i + 1]:
            return f"{EQUIVALENCIAS[sorted_freqs[i]]} y {EQUIVALENCIAS[sorted_freqs[i + 1]]}"
    if frequency < sorted_freqs[0]:
        return f"Por debajo de {EQUIVALENCIAS[sorted_freqs[0]]}"

# Comparar frecuencias con notas más cercanas
def compare_frequencies_closest(file="frequencies.json"):
    """Compara las frecuencias grabadas con las notas más cercanas."""
    try:
        with open(file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No se encontró el archivo de frecuencias.")
        return

    print("\nComparación de Frecuencias con Notas Más Cercanas:")
    for entry in data:
        freq = float(entry["frecuencia"])
        note, closest_freq = get_closest_note(freq)
        print(f"{entry['nombre']}: {freq} Hz -> Nota más cercana: {note} ({closest_freq} Hz)")

# Comparar frecuencias con rangos
def compare_frequencies_with_ranges(file="frequencies.json"):
    """Compara las frecuencias grabadas y determina su rango."""
    try:
        with open(file, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        print("No se encontró el archivo de frecuencias.")
        return

    print("\nComparación de Frecuencias con Rangos:")
    for entry in data:
        freq = float(entry["frecuencia"])
        note_range = get_note_range(freq)
        print(f"{entry['nombre']}: {freq} Hz -> Está entre {note_range}")

# Menú para elegir entre las opciones
def main_menu():
    """Muestra el menú principal para elegir las funcionalidades."""
    while True:
        print("\n--- Menú Principal ---")
        print("1. Comparar Frecuencias con Notas Más Cercanas")
        print("2. Comparar Frecuencias con Rangos")
        print("3. Salir")
        choice = input("Seleccione una opción: ")

        if choice == "1":
            compare_frequencies_closest()
        elif choice == "2":
            compare_frequencies_with_ranges()
        elif choice == "3":
            print("Saliendo del programa.")
            break
        else:
            print("Opción inválida. Intente nuevamente.")

# Ejecutar menú principal
if __name__ == "__main__":
    main_menu()
