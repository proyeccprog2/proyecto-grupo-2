import csv
import streamlit as st
import matplotlib.pyplot as plt

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

def estaciones_mas_caras(datos: list[dict], tipo: str, cantidad: int=5) -> list[dict]:
    """
    Dado un dataset, deuvelve una lista con las 'cantidad' estaciones mas caras de GNC.
    """
    print("obteniendo estaciones unicas")
    datos = obtener_estaciones_unicas(datos)
    estaciones = []
def obtener_estaciones_unicas(estaciones):
    unicas = []
    vistos = set()

    for est in estaciones:
        if (est["idempresa"]) not in vistos:
            unicas.append(est)
            vistos.add(est["idempresa"])

    return unicas

def dibujar_mas_caras(datos: list[dict]):
    st.subheader("top 5 estaciones más caras del país en GNC")

    top5 = estaciones_mas_caras(datos, "GNC")

    nombres = []
    precios = []
    colores = []
    #adicional si la estacion pertenece a YPF le agrega una estrellita ⭐ al nombre y se guarda el color azul para destacarla en el gráfico.


    for est in top5:
        nombre = f"{est['empresa']} ({est['provincia']})"
        if est["es_ypf"]:
            nombre += " (*)"
            colores.append("blue")
        else:
            colores.append("red")
        nombres.append(nombre)
        precios.append(est["precio"])

    fig, ax = plt.subplots()
    ax.bar(nombres, precios, color=colores)
    ax.set_xlabel("Estaciones")
    ax.set_ylabel("Precio ($/ litro)")
    ax.set_title("Top 5 estaciones más caras de GNC")
    plt.xticks(rotation=45, ha='right')

    st.pyplot(fig)

def main():
    # Cargar datos
    datos = leer_datos_csv("precios_surtidor_2024_2025_2026.csv")
    dibujar_mas_caras(datos)
# Ejecutar la aplicación
main()
