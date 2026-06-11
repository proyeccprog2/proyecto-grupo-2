import csv
import streamlit as st
import matplotlib.pyplot as plt

def leer_datos_csv(ruta):

    archivo = open(ruta, encoding="utf-8")

    lector = csv.DictReader(archivo)

    datos = []

    for fila in lector:

        fila["precio"] = float(fila["precio"])

        datos.append(fila)

    archivo.close()

    return datos
    # eliminamos si hay filas sin coordenadas
    dataset = [fila for fila in dataset
        if fila["latitud"].strip() != ""
        and fila["longitud"].strip() != ""]


#elimina empresas repetidas
def obtener_estaciones_unicas(estaciones):
    unicas =  []
#guardamos los idempresa 
    vistos = set()
#recorre todas las estaciones
    for est in estaciones:
        if est["idempresa"] not in vistos:
            unicas.append(est)
            vistos.add(est["idempresa"])
#DEVUELVE LAS UNICAS!!
    return unicas


def estaciones_mas_caras(datos, tipo, cantidad=5):
#elimina las estaciones repetidas con la funcion que hicimos antes
    datos = obtener_estaciones_unicas(datos)

    filtradas = []
#recorre todas las estacionessss
    for est in datos:
        #busca DEPENDIENDO EL COMBUSTIBLE QUE LE PIDAS
        if str(est["producto"]).upper() == tipo.upper():
            filtradas.append(est)

    resultado = []
#mientras no tenga 5
    while len(resultado) < cantidad and len(filtradas) > 0:
#suponemos que la primera esla mas cara
        mayor = filtradas[0]
#tratamos de encontrar una mas cara
        for est in filtradas:
            if est["precio"] > mayor["precio"]:
                mayor = est

        resultado.append(mayor)
        filtradas.remove(mayor)

    return resultado


def dibujar_mas_caras(datos):

    st.subheader("top 5 estaciones mas caras de GNC")

    top5 = estaciones_mas_caras(datos, "GNC")

    st.write("Cantidad de estaciones encontradas:", len(top5))
#si no encontro ninguna
    if len(top5) == 0:
        st.error("no se encontraron estaciones de GNC.")
        return

    nombres = []
    precios = []
#GUARDA TODO, NOMBRE Y PROVINCIA Y MAS ABAJO PRECIO
    for est in top5:
        nombres.append(
            f"{est['empresa']} ({est['provincia']})")
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

    st.title("combustibles")

    datos = leer_datos_csv(
        "precios_surtidor_2024_2025_2026.csv")

    dibujar_mas_caras(datos)

if __name__ == "__main__":
    main()
