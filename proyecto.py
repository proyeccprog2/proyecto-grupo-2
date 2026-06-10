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


def obtener_estaciones_unicas(estaciones):
    unicas = []
    vistos = set()

    for est in estaciones:
        if est["idempresa"] not in vistos:
            unicas.append(est)
            vistos.add(est["idempresa"])

    return unicas


def estaciones_mas_caras(datos: list[dict], tipo: str, cantidad: int = 5) -> list[dict]:
    """
    Devuelve las 'cantidad' estaciones más caras para un tipo de combustible.
    """

    datos = obtener_estaciones_unicas(datos)

    filtradas = []

    for est in datos:
        if est["producto"] == tipo.upper():
            filtradas.append(est)

    filtradas.sort(
        key=lambda estacion: estacion["precio"],
        reverse=True
    )

    return filtradas[:cantidad]


def dibujar_mas_caras(datos: list[dict]):

    st.subheader("Top 5 estaciones más caras del país en GNC")

    top5 = estaciones_mas_caras(datos, "GNC")

    nombres = []
    precios = []

    for est in top5:
        nombre = f"{est['empresa']} ({est['provincia']})"
        nombres.append(nombre)
        precios.append(est["precio"])

    fig, ax = plt.subplots()

    ax.bar(nombres, precios)

    ax.set_xlabel("Estaciones")
    ax.set_ylabel("Precio")
    ax.set_title("Top 5 estaciones más caras de GNC")

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    st.pyplot(fig)


def main():

    st.title("Análisis de combustibles")

    datos = leer_datos_csv(
        "precios_surtidor_2024_2025_2025.csv"
    )

    dibujar_mas_caras(datos)


if __name__ == "__main__":
    main()
