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

#definimos una funcion que recibe todos los datos y una provincia
#devuelve una lista con todas las estaciones de esa provincia, sin importar el combustible
def filtrar_estaciones_todas_por_provincia(datos: list[dict], provincia: str) -> list[dict]:
    #creamos una lista vacia donde vamos a guardar las estaciones de la provincia elegida
    resultado = []
    #recorremos todas las estaciones del dataset
    for estacion in datos:
    #si la provincia de la estacion coincide con la provincia elegida
        if estacion["provincia"] == provincia:
    #guardamos esa estacion en la lista resultado
            resultado.append(estacion)
    #devolvemos la lista con las estaciones filtradas
    return resultado


#definimos una funcion que recibe una lista de estaciones de una provincia
#y cuenta cuantas estaciones tiene cada marca/empresa
def contar_marcas_por_provincia(estaciones: list[dict]) -> dict:
#creamos un diccionario vacio donde vamos a guardar:
#LA clave = marca, valor = cantidad de estaciones de esa marca
    conteo = {}

#recorremos TODASS las estaciones
    for estacion in estaciones:
#guardamos en una variable el nombre de la empresa de esa estacion
        marca = estacion["empresa"]
        #si esa marca ya estaba en el diccionario, le sumamos 1
        if marca in conteo:
            conteo[marca] += 1
        else:
            #si aparece por primera vez le asignamos el valor 1
            conteo[marca] = 1

    #devolvemos el diccionario con el conteo de estaciones por marca
    return conteo
#encontramos el primer problema, que no podiamos poner TODAS las estaciones por la cantidad que eran
#se superponian entre si, entonces decidimos cambiar la pregunta a "¿Qué 5 marcas de estaciones de servicio tienen más presencia en una provincia seleccionada?"
#definimos una funcion que recibe un diccionario con marcas y cantidades
#se queda con las 5 marcas con mas presencia y agrupa el resto en "Otras"
def top_5_marcas(conteo_marcas: dict) -> dict:
#convertimos el diccionario en una lista de tuplas:
    #(marca, cantidad)
    marcas = list(conteo_marcas.items())

    #creamos un diccionario vacio donde vamos a guardar el resultado final
    resultado = {}

    #mientras no tengamos 5 marcas guardadas y todavia queden marcas por revisar
    while len(resultado) < 5 and len(marcas) > 0:
        #suponemos que la primera marca de la lista es la que mas estaciones tiene
        mayor = marcas[0]

    #recorremos la lista para buscar si hay una marca con mas estaciones
        for marca in marcas:
            if marca[1] > mayor[1]:
                mayor = marca

    #guardamos en el resultado la marca con mayor cantidad de estaciones
        resultado[mayor[0]] = mayor[1]

    #eliminamos esa marca de la lista para no volver a contarla
        marcas.remove(mayor)

    #si quedaron marcas afuera del top 5, las sumamos en "Otras"
    if marcas:
        suma_resto = 0
        for marca, cantidad in marcas:
            suma_resto += cantidad
        resultado["Otras"] = suma_resto

    #devolvemos el diccionario final con top 5 + otras
    return resultado

def dibujar_grafico_marcas(datos: list[dict]):
    st.subheader("Las 5 marcas con mayor presencia por provincia")

    # RECICLAMOS. usamos estaciones únicas para no contar varias veces la misma estación
    datos_unicos = obtener_estaciones_unicas(datos)

    # armamos el selectbox con las provincias
    provincias = sorted(obtener_campos_unicos(datos_unicos, "provincia"))
    provincia_elegida = st.selectbox("Seleccioná una provincia", provincias, key="prov_marcas")

    # filtramos las estaciones de la provincia elegida
    estaciones_provincia = filtrar_estaciones_todas_por_provincia(datos_unicos, provincia_elegida)

    # si no hay estaciones en esa provincia, mostramos advertencia
    if not estaciones_provincia:
        st.warning("no hay estaciones en esa provincia")
        return

    # contamos cuantas estaciones tiene cada marca
    conteo_marcas = contar_marcas_por_provincia(estaciones_provincia)

    # nos quedamos con el top 5 y agrupamos el resto en "Otras"
    conteo_top5 = top_5_marcas(conteo_marcas)

    marcas = list(conteo_top5.keys())
    cantidades = list(conteo_top5.values())

    total = sum(cantidades)

    # armamos los textos con porcentaje incluido
    leyenda = []
    for i in range(len(marcas)):
        porcentaje = (cantidades[i] / total) * 100
        leyenda.append(f"{marcas[i]} - {porcentaje:.1f}%")

    # dibujamos la torta SIN labels y SIN porcentajes adentro
    fig, ax = plt.subplots(figsize=(10, 8))

    wedges, _ = ax.pie(
        cantidades,
        startangle=90
    )

    ax.set_title(f"Distribución de estaciones por marca en {provincia_elegida} (top 5 + otras)")

    # agregamos la leyenda al costado
    ax.legend(
        wedges,
        leyenda,
        title="Marcas",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )

    plt.tight_layout()
    st.pyplot(fig)

# funcion que recibe los datos, una provincia y un combustible
# devuelve la estacion con el precio mas barato para esa combinación
def obtener_precio_mas_barato(datos: list[dict], provincia: str, combustible: str):
    # lista vacia donde vamos a guardar las estaciones que cumplen el filtro
    filtradas = []
    # recorremos todo el dataset buscando coincidencias de provincia y combustible
    for est in datos:
        if est["provincia"] == provincia and est["producto"] == combustible:
            filtradas.append(est)

    # si no encontramos ninguna estación que cumpla el filtro, devolvemos None
    if not filtradas:
        return None

    # suponemos que la primera estación es la mas barata
    estacion_barata = filtradas[0]

    # recorremos el resto buscando si hay una con menor precio
    for est in filtradas[1:]:
        if est["precio"] < estacion_barata["precio"]:
            estacion_barata = est

    # devolvemos un diccionario con los datos mas importantes de la estación encontrada
    return {
        "combustible": combustible,
        "provincia": provincia,
        "empresa": estacion_barata["empresa"],
        "localidad": estacion_barata["localidad"],
        "precio": estacion_barata["precio"]
    }


# funcion encargada de mostrar en Streamlit la estacion mas barata
# segun la provincia y el combustible seleccionado
def dibujar_precio_mas_barato(datos):
    st.subheader("Precio más barato por combustible en una provincia")

    # obtenemos todas las provincias disponibles en el dataset sin repetir
    provincias = sorted(obtener_campos_unicos(datos, "provincia"))

    #selector en la barra lateral para elegir provincia
    provincia = st.selectbox("Seleccioná una provincia", provincias, key="prov_barato")

    # obtenemos todos los tipos de combustible disponibles
    combustibles = sorted(obtener_campos_unicos(datos, "producto"))

    # selector en la barra lateral para elegir combustible
    combustible = st.selectbox("Seleccioná un combustible", combustibles, key="comb_barato")

    #llamamos a la función que busca la estación mas barata
    resultado = obtener_precio_mas_barato(datos, provincia, combustible)

    # si no hay datos para esa combinacion, mostramos
    if resultado is None:
        st.warning("no hay datos para esa selección")
        return

#mostramos un mensaje de éxito con el precio encontrado
    st.success(f"El precio mas barato de {combustible} en {provincia} es ${resultado['precio']}")

    # armamos una tabla con los datos de la estacionn encontrada
    tabla = [{
        "Combustible": resultado["combustible"],
        "Provincia": resultado["provincia"],
        "Empresa": resultado["empresa"],
        "Localidad": resultado["localidad"],
        "Precio por litro": resultado["precio"]
    }]

    # mostramos la tabla en Streamlit
    st.table(tabla)
def main():

    st.title("combustibles")

    datos = leer_datos_csv("precios_surtidor_2024_2025_2026.csv")
    dibujar_mapa(datos)
    dibujar_mas_caras(datos)
    dibujar_grafico_marcas(datos)
    dibujar_precio_mas_barato(datos)

if __name__ == "__main__":
    main()
