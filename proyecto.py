import csv
import streamlit as st
import matplotlib.pyplot as plt

def leer_datos_csv(ruta):
    archivo = open(ruta, encoding="utf-8")
    lector = csv.DictReader(archivo)
    datos = []
    # lista de las columnas que queremos descartar
    columnas_a_quitar = ["idtipohorario", "tipohorario", "fecha_vigencia", "geojson"]

    for fila in lector:

        fila["precio"] = float(fila["precio"])

        # creamos un diccionario vacío para ir guardando lo que si nos sirve
        fila_limpia = {}
        # revisa cada columna y su valor en la fila actual
        for clave, valor in fila.items():
            # si la columna NO es una de las que queremos quitar, la copiamos
            if clave not in columnas_a_quitar:
                fila_limpia[clave] = valor

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
        #suponemos que la primera es la mas cara
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
    #GUARDA TODOO, NOMBRE Y PROVINCIA Y MAS ABAJO PRECIO
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

############ Se puede testear
def obtener_campos_unicos(estaciones: list[dict], columna: str) -> list[str]:
    resultado = set()
    for estacion in estaciones:
        resultado.add(estacion[columna])
    return list(resultado)
    
######### Se puede testear
def filtrar_por_provincia_combustible(estaciones: list[dict], provincia: str, combustible: str) -> list[dict]:
    
    estaciones_filtradas = []
    for estacion in estaciones:
        if (estacion["provincia"] == provincia and estacion["producto"] == combustible):
            estaciones_filtradas.append(estacion)
    return estaciones_filtradas

######### Se puede testear
def obtener_estacion_barata(estaciones: list[dict], provincia: str, combustible: str) -> list[dict]:
    estaciones_filtradas = filtrar_por_provincia_combustible(estaciones, provincia, combustible)
    resultado = []

    if estaciones_filtradas:
        precio = estaciones_filtradas[0]["precio"]
        estacion_barata = estaciones_filtradas[0]
        estacion_barata = {"lat": float(estaciones_filtradas[0]["latitud"]),
                           "lon": float(estaciones_filtradas[0]["longitud"]),
                           "localidad": estaciones_filtradas[0]["localidad"]}

        for estacion in estaciones_filtradas[1:]:
            if estacion["precio"] < precio:
                precio = estacion["precio"]
                estacion_barata = {"lat": float(estacion["latitud"]),
                                   "lon": float(estacion["longitud"]),
                                   "localidad": estacion["localidad"]}

        resultado.append(estacion_barata)

    return resultado

def dibujar_mapa(datos: list[dict]):
    st.title("Estaciones de GNC en Argentina")

    # sidebar para filtros
    opcion = st.sidebar.radio(
        "Uso del mapa",
        ["Mapa de GNC", "Ciudad más barata"],
        key="visibility"
    )

    # y recorremos todas las filas tomando unicamente las provincias que tienen estaciones de gnc
    #usamos "sorted()" para que aparezcan ordenadas alfabeticamente
    #selectbox
    provincias = sorted(obtener_campos_unicos(datos, "provincia"))
    provincia_elegida = st.sidebar.selectbox("Porfavor seleccioná una provincia", provincias)

    if opcion == "Mapa de GNC":
        # Mapa visualizando las estaciones de GNC de la provincia seleccionada
        st.subheader(f"Estaciones de GNC en {provincia_elegida}")
        estaciones_en_mapa = filtrar_estaciones_por_provincia(datos, provincia_elegida)
        #si encontre las estaciones, vamos a dibujar el mapita
        if estaciones_en_mapa:
            st.map(estaciones_en_mapa)
            #pero si no hay datos mostramos una advertencia
        else:
            # Si no se encuentran estaciones se muestra una advertencia y se muestra el mapa general de argentina
            st.warning("No se encontraron estaciones para esta provincia")
            default = [{"lat":-38.416097, "lon": -63.616672}] # Centro de Argentina
            st.map(data = default, color = "#00000000", zoom = 3) # El color usado es 100% transparente
            
    elif opcion == "Ciudad más barata":
        combustibles = sorted(obtener_campos_unicos(datos, "producto"))
        combustible_elegido = st.sidebar.selectbox("Porfavor seleccioná el tipo de combustible", combustibles)

        # Mapa visualizando la estación con el precio más barato del combustible y la provincia elegidos
        estacion_barata = obtener_estacion_barata(datos, provincia_elegida, combustible_elegido)
        # si encuentra las estaciones, vamos a dibujar el mapita
        if estacion_barata:
            st.subheader(f"La estación de '{combustible_elegido}' más barata en {provincia_elegida}, está en la localidad de {estacion_barata[0]["localidad"]}")
            st.map(estacion_barata)
        else:
            # Si no se encuentran estaciones se muestra una advertencia y se muestra el mapa general de argentina
            st.warning(f"No se encontraron estaciones de {combustible_elegido} en {provincia_elegida}")
            default = [{"lat":-38.416097, "lon": -63.616672}] # Centro de Argentina
            st.map(data = default, color = "#00000000", zoom = 3) # El color usado es 100% transparente


def main():

    st.title("combustibles")

    datos = leer_datos_csv(
        "precios_surtidor_2024_2025_2026.csv")
    dibujar_mapa(datos)
    dibujar_mas_caras(datos)

if __name__ == "__main__":
    main()
