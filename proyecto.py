import csv
import streamlit as st
import matplotlib.pyplot as plt

def leer_datos_csv(ruta):

    archivo = open(ruta)

    encabezados = archivo.readline().strip().split(",")

    datos = []

    linea = archivo.readline()

    while linea != "":

        valores = linea.strip().split(",")

        registro = {}

        i = 0
        while i < len(encabezados):
            registro[encabezados[i]] = valores[i]
            i += 1

        datos.append(registro)

        linea = archivo.readline()

    archivo.close()

    return datos

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


def estaciones_mas_caras(datos, tipo, cantidad=5):

    datos = obtener_estaciones_unicas(datos)

    filtradas = []

    for est in datos:
        if str(est["producto"]).upper() == tipo.upper():
            filtradas.append(est)

    resultado = []

    while len(resultado) < cantidad and len(filtradas) > 0:

        mayor = filtradas[0]

        for est in filtradas:
            if est["precio"] > mayor["precio"]:
                mayor = est

        resultado.append(mayor)
        filtradas.remove(mayor)

    return resultado


def dibujar_mas_caras(datos):

    st.subheader("Top 5 estaciones más caras de GNC")

    top5 = estaciones_mas_caras(datos, "GNC")

    st.write("Cantidad de estaciones encontradas:", len(top5))

    if len(top5) == 0:
        st.error("No se encontraron estaciones de GNC.")
        return

    nombres = []
    precios = []

    for est in top5:
        nombres.append(
            f"{est['empresa']} ({est['provincia']})"
        )
        precios.append(est["precio"])

    fig, ax = plt.subplots()

    ax.bar(nombres, precios)

    ax.set_xlabel("Estación")
    ax.set_ylabel("Precio")
    ax.set_title("Top 5 estaciones más caras de GNC")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)


def main():

    st.title("Análisis de Combustibles")

    datos = leer_datos_csv(
        "precios_surtidor_2024_2025_2026.csv"
    )

    dibujar_mas_caras(datos)

if __name__ == "__main__":
    main()
