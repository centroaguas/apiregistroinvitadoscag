import csv
import qrcode
import os

# --- Configuración ---
ARCHIVO_CSV = 'datosempleadosadd.csv'  # Nombre de tu archivo CSV
COLUMNA_CEDULA = 'cedula'     # Nombre de la columna de la cédula
COLUMNA_NOMBRE = 'nombre'      # Nombre de la columna del nombre
DIRECTORIO_SALIDA = 'codigos_qr'  # Directorio donde se guardarán los códigos QR


def generar_codigos_qr_desde_csv(archivo_csv, col_cedula, col_nombre, dir_salida):
    """
    Genera códigos QR a partir de un archivo CSV.
    El contenido del QR será la cédula y el nombre.
    El nombre del archivo PNG será la cédula.
    """

    # 1. Crear el directorio de salida si no existe
    if not os.path.exists(dir_salida):
        os.makedirs(dir_salida)
        print(f"Directorio '{dir_salida}' creado.")

    try:
        with open(archivo_csv, mode='r', encoding='utf-8') as file:
            # Usar DictReader para leer el CSV como un diccionario,
            # utilizando los encabezados como claves.
            reader = csv.DictReader(file)

            contador = 0

            for fila in reader:
                try:
                    # 2. Obtener los datos de las columnas
                    cedula = fila[col_cedula].strip()
                    nombre = fila[col_nombre].strip()

                    # El contenido del código QR será la combinación de cédula y nombre
                    # datos_qr = f"{cedula} - {nombre}"
                    datos_qr = f"{cedula}"

                    # 3. Configurar el objeto QR
                    qr = qrcode.QRCode(
                        # Tamaño del QR (1 es pequeño, aumenta complejidad)
                        version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de error
                        box_size=10,  # Tamaño de cada "caja" o módulo
                        border=4,  # Grosor del borde
                    )

                    # 4. Añadir los datos y generar el código
                    qr.add_data(datos_qr)
                    qr.make(fit=True)

                    # Crear la imagen
                    img = qr.make_image(fill_color="black", back_color="white")

                    # 5. Guardar el archivo PNG con el número de cédula como nombre
                    nombre_archivo = os.path.join(dir_salida, f"{cedula}.png")
                    img.save(nombre_archivo)

                    print(
                        f"QR generado para Cédula: {cedula} y Nombre: {nombre} -> {nombre_archivo}")
                    contador += 1

                except KeyError as e:
                    print(
                        f"Error: La columna {e} no se encontró en el archivo CSV. Verifica la configuración.")
                    break
                except Exception as e:
                    print(
                        f"Error al procesar la fila con cédula '{cedula}': {e}")

            print(
                f"\n--- Proceso Finalizado. {contador} códigos QR generados. ---")

    except FileNotFoundError:
        print(f"Error: El archivo '{archivo_csv}' no se encontró.")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")


# Ejecutar la función principal
if __name__ == "__main__":
    generar_codigos_qr_desde_csv(
        ARCHIVO_CSV, COLUMNA_CEDULA, COLUMNA_NOMBRE, DIRECTORIO_SALIDA)
