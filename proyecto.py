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
############ elegimos la siguiente funcion para testear porque es una funcion pura, recibe estaciones
#y devuelve otra lista SIN REPETIR. 
#elimina empresas repetidas
def obtener_estaciones_unicas(estaciones):
    unicas =  []
#guardamos los idemprecuitsa
    vistos = set()
#recorre todas las estaciones
    for est in estaciones:
        if est["idemprecuitsa"] not in vistos:
            unicas.append(est)
            vistos.add(est["idemprecuitsa"])
#DEVUELVE LAS UNICAS!!
    return unicas
##TEST 
#testeamos que la funcion elimine las empresas repetidas
def test_obtener_estaciones_unicas():
    estaciones = [
        {"idemprecuitsa": "1"},
        {"idemprecuitsa": "1"},
        {"idemprecuitsa": "2"}
    ]

    assert len(obtener_estaciones_unicas(estaciones)) == 2

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

    ax.set_ylabel("Precio")
    ax.set_title("Top 5 estaciones más caras de GNC")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
#definimos una funcion que recibe los datos del csv y una provincia ELEGIDA
def filtrar_estaciones_por_provincia(datos: list[dict], provincia: str) -> list[dict]:
    """
    recibe un dataset y transforma los datos de las coordenadas en geoposionamineto para luego poder usarlo
    en el mapa
    """
#creamos una lista vacia para luego guardar los datos que nos interesa
    resultado = []
#recorremos todas las filas del dataset y nos frenamos unicamente en las que venden GNC y verificamos que
#aparezcan en la provincia SELECCIONADA
    for fila in datos:
        if fila["producto"] == "GNC" and fila["provincia"] == provincia:
#AGREGO LAS CORDENADAS A LA LISTA RESULTADO
#USAMOS FLOAT PORQUE EN EL CSV VIENEN COMO TEXTO Y PARA EL MAPA VAMOS A NECESITAR NUMEROS          
            resultado.append({
                "lat": float(fila["latitud"]),
                "lon": float(fila["longitud"])
            })
#DEVUELVO LA LISTA CON TODAS LAS COORDENADAS ENCONTRADAS
    return resultado
    
def dibujar_mapa(datos: list[dict]):
    st.title("Estaciones de GNC en Argentina")

    # sidebar  para filtrar por provincia
    # y recorremos todas las filas tomandoi unicamente las provincias que tienen estaciones de gnc
    #usamos "sorted()" para que aparezcan ordenadas alfabeticamente
    provincias = sorted({fila["provincia"] for fila in datos if fila["producto"] == "GNC"})
    #selectbox
    provincia_elegida = st.sidebar.selectbox("Porfavor seleccioná una provincia", provincias)

    # mapa visualizando las estaciones de GNC de la provincia seleccionada
    st.subheader(f"Estaciones de GNC en {provincia_elegida}")
    estaciones_en_mapa = filtrar_estaciones_por_provincia(datos, provincia_elegida)
#si encontre las estaciones, vamos a dibujar el mapita
    if estaciones_en_mapa:
        st.map(estaciones_en_mapa)
    #pero si no hay datos mostramos una advertencia
    else:
        st.warning("No se encontraron estaciones con coordenadas para esta provincia")

def main():

    st.title("combustibles")

    datos = leer_datos_csv(
        "precios_surtidor_2024_2025_2026.csv")
    dibujar_mapa(datos)
    dibujar_mas_caras(datos)

if __name__ == "__main__":
    main()
