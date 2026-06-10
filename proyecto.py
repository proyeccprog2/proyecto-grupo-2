import csv


def leer_datos_csv(ruta: str) -> list[dict]:

    with open(ruta, newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        dataset = list(lector)

    # Eliminar filas sin coordenadas
    dataset = [
        fila
        for fila in dataset
        if fila["latitud"].strip() != ""
        and fila["longitud"].strip() != ""
    ]

    # Limpiar y convertir datos
    for diccionario in dataset:
        for clave, valor in diccionario.items():

            valor = valor.strip()

            try:
                diccionario[clave] = float(valor)
            except ValueError:
                diccionario[clave] = valor.upper()

    return dataset

datos = leer_datos_csv("precios_surtidor_2024_2025_2026.csv")

print(len(datos))
print(datos[0])