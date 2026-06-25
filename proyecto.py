import csv
import streamlit as st
import matplotlib.pyplot as plt


def leer_datos_csv(ruta):
    '''
    Diseño de datos:
    ruta: string

    Signatura:
    leer_datos_csv: str -> list[dict]

    Propósito:
    lee un archivo CSV con información de estaciones de servicio,
    convierte el campo precio a float y devuelve una lista de
    diccionarios con los datos.

    Ejemplo:
    leer_datos_csv("precios_surtidor_2024_2025_2026.csv") =
    [{"empresa":"BLESER S.R.L.",
    "provincia":"BUENOS AIRES",
    "producto":"GNC",
    "precio":579.0,
    ...}]
    '''
    archivo = open(ruta, encoding="utf-8")
    lector = csv.DictReader(archivo)
    datos = []
    columnas_a_quitar = ["idtipohorario", "tipohorario", "fecha_vigencia", "geojson"]

    for fila in lector:
        fila["precio"] = float(fila["precio"])

        fila_limpia = {}
        for clave, valor in fila.items():
            if clave not in columnas_a_quitar:
                fila_limpia[clave] = valor

        datos.append(fila_limpia)

    archivo.close()
    return datos
#definimos una funcion general para filtrar estaciones
#sirve para filtrar por provincia, por combustible o por ambas cosas a la vez
#definimos una funcion que recibe los datos del csv y una provincia ELEGIDA
def filtrar_estaciones_por_provincia(datos: list[dict], provincia: str) -> list[dict]:
    '''
    Propósito:
    filtra las estaciones de GNC pertenecientes a una provincia
    y devuelve sus coordenadas para ser utilizadas en el mapa.


    Ejemplo:
    filtrar_estaciones_por_provincia(datos,"BUENOS AIRES") =
    [{"lat":-35.1234,"lon":-58.5678}, ...]
    '''
    resultado = []
    for fila in datos:
        if fila["producto"] == "GNC" and fila["provincia"] == provincia:
            resultado.append({
                "lat": float(fila["latitud"]),
                "lon": float(fila["longitud"])
            })
    return resultado

def filtrar_estaciones(estaciones: list[dict], provincia=None, combustible=None) -> list[dict]:
    '''
    Propósito:
    filtra estaciones según provincia y/o combustible.

    Si provincia tiene valor, solo deja las estaciones de esa provincia.
    Si combustible tiene valor, solo deja las estaciones de ese combustible.
    Si ambos tienen valor, deben cumplirse las dos condiciones.

    Ejemplos:
    filtrar_estaciones(datos, provincia="BUENOS AIRES")
    filtrar_estaciones(datos, combustible="GNC")
    filtrar_estaciones(datos, provincia="BUENOS AIRES", combustible="GNC")
    '''
    #creamos una lista vacia donde vamos a guardar las estaciones que cumplan
    resultado = []

    #recorremos todas las estaciones
    for estacion in estaciones:
        #suponemos que la estacion cumple
        cumple = True

        #si nos pasaron una provincia, verificamos que coincida
        if provincia != None and estacion["provincia"] != provincia:
            cumple = False

        #si nos pasaron un combustible, verificamos que coincida
        if combustible != None and estacion["producto"] != combustible:
            cumple = False

        #si cumplio todas las condiciones, la guardamos
        if cumple:
            resultado.append(estacion)

    #devolvemos la lista filtrada
    return resultado
############ elegimos la siguiente funcion para testear porque es una funcion pura, recibe estaciones
# y devuelve otra lista SIN REPETIR.
# elimina empresas repetidas
def obtener_estaciones_unicas(estaciones):
    '''
    Diseño de datos:
    estaciones: List[dict]

    Signatura:
    obtener_estaciones_unicas: List[dict] -> List[dict]

    Propósito:
    recibe una lista de estaciones y devuelve otra lista sin
    repeticiones según el campo idemprecuitsa.

    Ejemplo:
    obtener_estaciones_unicas(estaciones) = [{"idemprecuitsa":"1"}, {"idemprecuitsa":"2"}]
    '''
    unicas = []
    # guardamos los idemprecuitsa
    vistos = set()
    # recorre todas las estaciones
    for est in estaciones:
        if est["idemprecuitsa"] not in vistos:
            unicas.append(est)
            vistos.add(est["idemprecuitsa"])
    # DEVUELVE LAS UNICAS!!
    return unicas


######### Se puede testear
def obtener_campos_unicos(estaciones: list[dict], columna: str) -> list[str]:
    '''
    Propósito:
    obtiene todos los valores únicos de una columna del dataset.

    Ejemplo:
    obtener_campos_unicos(estaciones,"provincia") =
    ["BUENOS AIRES",
    "CATAMARCA",
    "CHACO",
    "CHUBUT",
    ...]
    '''
    resultado = set()
    for estacion in estaciones:
        resultado.add(estacion[columna])
    return list(resultado)

# definimos una funcion general que obtiene las estaciones mas baratas o mas caras
def obtener_top_por_precio(estaciones: list[dict], cantidad: int, mas_baratas: bool) -> list[dict]:
    '''
    Propósito:
    devuelve una lista con las estaciones mas baratas o mas caras
    segun el valor de mas_baratas.

    Si mas_baratas es True -> devuelve las mas baratas
    Si mas_baratas es False -> devuelve las mas caras

    Ejemplo:
    obtener_top_por_precio(estaciones, 3, True) = [3 estaciones mas baratas]
    obtener_top_por_precio(estaciones, 5, False) = [5 estaciones mas caras]
    '''
    # hacemos una copia de la lista para no modificar la original
    estaciones_restantes = []
    for estacion in estaciones:
        estaciones_restantes.append(estacion)

    resultado = []

    # mientras no tengamos la cantidad pedida y todavia queden estaciones
    while len(resultado) < cantidad and len(estaciones_restantes) > 0:
        # suponemos que la primera es la mejor candidata
        elegida = estaciones_restantes[0]

        # recorremos todas las estaciones restantes buscando una mejor
        for estacion in estaciones_restantes:
            # si queremos las mas baratas, buscamos el menor precio
            if mas_baratas:
                if estacion["precio"] < elegida["precio"]:
                    elegida = estacion
            # si queremos las mas caras, buscamos el mayor precio
            else:
                if estacion["precio"] > elegida["precio"]:
                    elegida = estacion

        # guardamos la estacion encontrada
        resultado.append(elegida)

        # la eliminamos para no repetirla
        estaciones_restantes.remove(elegida)

    return resultado


def estaciones_mas_caras(datos, tipo, cantidad=5):
    '''
    Diseño de datos:
    datos: List[dict]
    tipo: string
    cantidad: int

    Signatura:
    estaciones_mas_caras:
    List[diccionario] string int -> List[diccionario]

    Propósito:
    obtiene las estaciones con el precio más alto para el tipo
    de combustible indicado.

    Ejemplo:
    estaciones_mas_caras(datos, "GNC", 5) = [{"empresa":"YPF","precio":1500.0,...}]
    '''
    # elimina las estaciones repetidas
    datos_unicos = obtener_estaciones_unicas(datos)

    # filtramos solo las estaciones del combustible elegido
    filtradas = filtrar_estaciones(datos_unicos, combustible=tipo)

    # usamos la funcion general para obtener las mas caras
    return obtener_top_por_precio(filtradas, cantidad, False)


def dibujar_mas_caras(datos):
    st.subheader("Top 5 estaciones más caras de GNC")

    top5 = estaciones_mas_caras(datos, "GNC")

    # si no encontró ninguna
    if len(top5) == 0:
        st.error("No se encontraron estaciones de GNC.")
        return

    nombres = []
    precios = []

    # guarda nombre y provincia
    for est in top5:
        nombres.append(f"{est['empresa']} ({est['provincia']})")
        precios.append(est["precio"])

    fig, ax = plt.subplots()

    ax.bar(nombres, precios)

    ax.set_ylabel("Precio")
    ax.set_title("Top 5 estaciones más caras de GNC")

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)


def obtener_estacion_barata(estaciones: list[dict], provincia: str, combustible: str) -> list[dict]:
    '''
    Propósito:
    busca la estación más barata para una provincia y combustible
    determinados y devuelve su ubicación.

    Ejemplo:
    obtener_estacion_barata(estaciones,"BUENOS AIRES","GNC") =
    [{"lat":-35.1234,
    "lon":-58.5678,
    "localidad":"LA PLATA"}]
    '''
    # filtramos por provincia y combustible
    estaciones_filtradas = filtrar_estaciones(estaciones, provincia, combustible)
    # si no hay estaciones devolvemos lista vacia
    if not estaciones_filtradas:
        return []

    # obtenemos la estacion mas barata usando la funcion general
    estacion_barata = obtener_top_por_precio(estaciones_filtradas, 1, True)[0]

    # devolvemos el formato que necesita el mapa
    return [{
        "lat": float(estacion_barata["latitud"]),
        "lon": float(estacion_barata["longitud"]),
        "localidad": estacion_barata["localidad"]
    }]


def dibujar_mapa(datos: list[dict]):
    st.title("Estaciones de GNC en Argentina")

    # sidebar para filtros
    opcion = st.sidebar.radio(
        "Uso del mapa",
        ["Mapa de GNC", "Ciudad más barata"],
        key="visibility"
    )

    # selectbox de provincias
    provincias = sorted(obtener_campos_unicos(datos, "provincia"))
    provincia_elegida = st.sidebar.selectbox("Por favor seleccioná una provincia", provincias)

    if opcion == "Mapa de GNC":
        # mapa visualizando las estaciones de GNC de la provincia seleccionada
        st.subheader(f"Estaciones de GNC en {provincia_elegida}")
        estaciones_en_mapa = filtrar_estaciones_por_provincia(datos, provincia_elegida)

        # si encontré estaciones, dibujo el mapa
        if estaciones_en_mapa:
            st.map(estaciones_en_mapa)
        else:
            # si no hay estaciones, mostramos advertencia y un mapa general
            st.warning("No se encontraron estaciones para esta provincia")
            default = [{"lat": -38.416097, "lon": -63.616672}]  # centro de Argentina
            st.map(data=default, color="#00000000", zoom=3)

    elif opcion == "Ciudad más barata":
        combustibles = sorted(obtener_campos_unicos(datos, "producto"))
        combustible_elegido = st.sidebar.selectbox("Por favor seleccioná el tipo de combustible", combustibles)

        # mapa visualizando la estación con el precio más barato
        estacion_barata = obtener_estacion_barata(datos, provincia_elegida, combustible_elegido)

        if estacion_barata:
            st.subheader(
                f"La estación de '{combustible_elegido}' más barata en {provincia_elegida}, "
                f"está en la localidad de {estacion_barata[0]['localidad']}"
            )
            st.map(estacion_barata)
        else:
            st.warning(f"No se encontraron estaciones de {combustible_elegido} en {provincia_elegida}")
            default = [{"lat": -38.416097, "lon": -63.616672}]
            st.map(data=default, color="#00000000", zoom=3)


# definimos una funcion que recibe una lista de estaciones de una provincia
# y cuenta cuantas estaciones tiene cada marca/empresa
def contar_marcas_por_provincia(estaciones: list[dict]) -> dict:
    '''
    Propósito:
    cuenta cuántas estaciones posee cada empresa dentro de una
    provincia.

    Ejemplo:
    contar_marcas_por_provincia(estaciones) =
    {"YPF":120,
    "SHELL":58,
    "AXION":44}
    '''
    # creamos un diccionario vacio donde vamos a guardar:
    # clave = marca, valor = cantidad de estaciones de esa marca
    conteo = {}

    # recorremos todas las estaciones
    for estacion in estaciones:
        # guardamos en una variable el nombre de la empresa de esa estacion
        marca = estacion["empresa"]

        # si esa marca ya estaba en el diccionario, le sumamos 1
        if marca in conteo:
            conteo[marca] += 1
        else:
            # si aparece por primera vez le asignamos el valor 1
            conteo[marca] = 1

    # devolvemos el diccionario con el conteo de estaciones por marca
    return conteo


# encontramos el primer problema, que no podiamos poner TODAS las estaciones por la cantidad que eran
# se superponian entre si, entonces decidimos cambiar la pregunta a
# "¿Qué 5 marcas de estaciones de servicio tienen más presencia en una provincia seleccionada?"
# definimos una funcion que recibe un diccionario con marcas y cantidades
# se queda con las 5 marcas con mas presencia y agrupa el resto en "Otras"
def top_5_marcas(conteo_marcas: dict) -> dict:
    '''
    Propósito:
    obtiene las cinco marcas con mayor cantidad de estaciones y
    agrupa el resto en la categoría "Otras".

    Ejemplo:
    top_5_marcas({"YPF":120,"SHELL":58,"AXION":44,"PUMA":31,"GULF":18,"OTRA":12}) =
    {"YPF":120,"SHELL":58,"AXION":44,"PUMA":31,"GULF":18,"Otras":12}
    '''
    # convertimos el diccionario en una lista de tuplas:
    # (marca, cantidad)
    marcas = list(conteo_marcas.items())

    # creamos un diccionario vacio donde vamos a guardar el resultado final
    resultado = {}

    # mientras no tengamos 5 marcas guardadas y todavia queden marcas por revisar
    while len(resultado) < 5 and len(marcas) > 0:
        # suponemos que la primera marca de la lista es la que mas estaciones tiene
        mayor = marcas[0]

        # recorremos la lista para buscar si hay una marca con mas estaciones
        for marca in marcas:
            if marca[1] > mayor[1]:
                mayor = marca

        # guardamos en el resultado la marca con mayor cantidad de estaciones
        resultado[mayor[0]] = mayor[1]

        # eliminamos esa marca de la lista para no volver a contarla
        marcas.remove(mayor)

    # si quedaron marcas afuera del top 5, las sumamos en "Otras"
    if marcas:
        suma_resto = 0
        for marca, cantidad in marcas:
            suma_resto += cantidad
        resultado["Otras"] = suma_resto

    # devolvemos el diccionario final con top 5 + otras
    return resultado


def dibujar_grafico_marcas(datos: list[dict]):
    st.subheader("Las 5 marcas con mayor presencia por provincia")

    # usamos estaciones únicas para no contar varias veces la misma estación
    datos_unicos = obtener_estaciones_unicas(datos)

    # armamos el selectbox con las provincias
    provincias = sorted(obtener_campos_unicos(datos_unicos, "provincia"))
    provincia_elegida = st.selectbox("Seleccioná una provincia", provincias, key="prov_marcas")

    # filtramos las estaciones de la provincia elegida
    estaciones_provincia = filtrar_estaciones(datos_unicos, provincia=provincia_elegida)

    # si no hay estaciones en esa provincia, mostramos advertencia
    if not estaciones_provincia:
        st.warning("No hay estaciones en esa provincia")
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

    ax.set_title(f"Distribución de estaciones por marca en {provincia_elegida} (Top 5 + Otras)")

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
# devuelve las 5 estaciones con el precio mas barato para esa combinación
def obtener_precio_mas_barato(datos: list[dict], provincia: str, combustible: str) -> list[dict]:
    '''
    Diseño de datos:
    datos: List[diccionario]
    provincia: string
    combustible: string

    Signatura:
    obtener_precio_mas_barato:
    List[diccionario] string string -> List[diccionario]

    Propósito:
    busca las 5 estaciones con el precio más barato para una provincia
    y combustible determinados.

    Ejemplos:
    obtener_precio_mas_barato(datos, "BUENOS AIRES","GNC") =
    [
        {"combustible":"GNC","provincia":"BUENOS AIRES","empresa":"X","localidad":"LA PLATA","precio":579.0},
        {"combustible":"GNC","provincia":"BUENOS AIRES","empresa":"Y","localidad":"QUILMES","precio":581.0}
    ]
    '''
    # filtramos por provincia y combustible
    filtradas = filtrar_estaciones(datos, provincia, combustible)
    # si no encontramos estaciones devolvemos lista vacia
    if not filtradas:
        return []

    # obtenemos las 5 estaciones mas baratas
    top5_baratas = obtener_top_por_precio(filtradas, 5, True)

    resultado = []

    # armamos la lista con el formato que queremos mostrar en la tabla
    for estacion in top5_baratas:
        resultado.append({
            "combustible": combustible,
            "provincia": provincia,
            "empresa": estacion["empresa"],
            "localidad": estacion["localidad"],
            "precio": estacion["precio"]
        })

    return resultado


# funcion encargada de mostrar en Streamlit las 5 estaciones mas baratas
# segun la provincia y el combustible seleccionado
def dibujar_precio_mas_barato(datos):
    st.subheader("Top 5 precios más baratos por combustible en una provincia")

    # obtenemos todas las provincias disponibles en el dataset sin repetir
    provincias = sorted(obtener_campos_unicos(datos, "provincia"))

    # selector para elegir provincia
    provincia = st.selectbox("Seleccioná una provincia", provincias, key="prov_barato")

    # obtenemos todos los tipos de combustible disponibles
    combustibles = sorted(obtener_campos_unicos(datos, "producto"))

    # selector para elegir combustible
    combustible = st.selectbox("Seleccioná un combustible", combustibles, key="comb_barato")

    # llamamos a la función que busca las 5 estaciones mas baratas
    resultados = obtener_precio_mas_barato(datos, provincia, combustible)

    # si no hay datos para esa combinacion, mostramos advertencia
    if not resultados:
        st.warning("No hay datos para esa selección")
        return

    # mostramos el precio mas barato de todos los encontrados
    st.success(f"El precio más barato de {combustible} en {provincia} es ${resultados[0]['precio']}")

    # armamos la tabla con las estaciones encontradas
    tabla = []

    for resultado in resultados:
        tabla.append({
            "Combustible": resultado["combustible"],
            "Provincia": resultado["provincia"],
            "Empresa": resultado["empresa"],
            "Localidad": resultado["localidad"],
            "Precio por litro": resultado["precio"]
        })

    # mostramos la tabla en Streamlit
    st.table(tabla)


def ordenar_promedios(promedios: list[dict]):
    '''
    Diseño de datos:
    promedios: List[dict]

    Signatura:
    ordenar_promedios:
    List[diccionario] -> List[diccionario]

    Propósito:
    ordena una lista de estaciones según su precio promedio
    de mayor a menor

    Ejemplo:
    ordenar_promedios([{"empresa":"YPF","precio_promedio":1200.0},
    {"empresa":"SHELL","precio_promedio":1500.0},
    {"empresa":"AXION","precio_promedio":1300.0}]) =
    [{"empresa":"SHELL","precio_promedio":1500.0},
    {"empresa":"AXION","precio_promedio":1300.0},
    {"empresa":"YPF","precio_promedio":1200.0}]
    '''
    n = len(promedios)
    for i in range(n):
        for j in range(0, n - i - 1):
            # si el precio actual es MENOR al siguiente, los intercambiamos
            # así los más caros van quedando al principio de la lista
            if promedios[j]["precio_promedio"] < promedios[j + 1]["precio_promedio"]:
                aux = promedios[j]
                promedios[j] = promedios[j + 1]
                promedios[j + 1] = aux

    return promedios


def obtener_10_promedios_altos(estaciones: list[dict]) -> list[dict]:
    '''
    Propósito:
    calcula el precio promedio de los combustibles para cada
    estación de servicio y devuelve las 10 estaciones con los
    promedios más altos

    Ejemplo:
    obtener_10_promedios_altos(estaciones) =
    [{"empresa":"YPF","precio_promedio":1450.0},
    {"empresa":"SHELL","precio_promedio":1420.0},
    {"empresa":"AXION","precio_promedio":1385.0},
    ...
    ]
    '''
    agrupados = {}

    for estacion in estaciones:
        id_est = estacion["idemprecuitsa"]

        if id_est not in agrupados:
            agrupados[id_est] = {
                "empresa": estacion["empresa"],
                "suma_precios": 0,
                "cantidad": 0
            }

        agrupados[id_est]["suma_precios"] += estacion["precio"]
        agrupados[id_est]["cantidad"] += 1

    promedios = []

    for id_est, info in agrupados.items():
        promedio = info["suma_precios"] / info["cantidad"]
        promedios.append({
            "empresa": info["empresa"],
            "precio_promedio": promedio
        })

    promedios = ordenar_promedios(promedios)
    return promedios[:10]


def dibujar_promedios_altos(datos: list[dict]):
    st.subheader("Top 10 estaciones con el precio promedio más alto")

    top10 = obtener_10_promedios_altos(datos)

    nombres = []
    precios = []

    # preparamos las listas para el gráfico
    for est in top10:
        etiqueta = str(est['empresa'])
        nombres.append(etiqueta)
        precios.append(est["precio_promedio"])

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(nombres, precios, color='salmon')

    ax.set_ylabel("Precio Promedio ($)")
    ax.set_title("Estaciones más caras del país (Promedio de todos sus combustibles)")

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    st.pyplot(fig)


def main():
    st.title("Combustibles")

    datos = leer_datos_csv("precios_surtidor_2024_2025_2026.csv")
    dibujar_mapa(datos)
    dibujar_mas_caras(datos)
    dibujar_promedios_altos(datos)
    dibujar_grafico_marcas(datos)
    dibujar_precio_mas_barato(datos)


if __name__ == "__main__":
    main()