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


def estaciones_mas_caras(datos, tipo, cantidad=5):

    datos = obtener_estaciones_unicas(datos)

    filtradas = []

    for est in datos:
        if "producto" in est:
            if str(est["producto"]).upper() == tipo.upper():
                filtradas.append(est)

    filtradas.sort(
        key=lambda x: x["precio"],
        reverse=True
    )

    return filtradas[:cantidad]


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


    dibujar_mas_caras(datos)

    except Exception as e:
        st.error(f"Ocurrió un error: {e}")


if __name__ == "__main__":
    main()