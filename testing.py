from proyecto import (
    obtener_estaciones_unicas,
    filtrar_estaciones_por_provincia,
    contar_marcas_por_provincia,
    obtener_precio_mas_barato,
    obtener_estacion_barata,
    obtener_campos_unicos,
    ordenar_promedios,
    obtener_10_promedios_altos
)


def test_obtener_estaciones_unicas():
    estaciones1 = [
        {"idemprecuitsa": "1"},
        {"idemprecuitsa": "1"},
        {"idemprecuitsa": "2"}
    ]

    estaciones2 = [
        {"idemprecuitsa": "7"},
        {"idemprecuitsa": "5"},
        {"idemprecuitsa": "3"},
        {"idemprecuitsa": "4"},
        {"idemprecuitsa": "3"}
    ]

    assert obtener_estaciones_unicas(estaciones1) == [
        {"idemprecuitsa": "1"},
        {"idemprecuitsa": "2"}
    ]

    assert obtener_estaciones_unicas(estaciones2) == [
        {"idemprecuitsa": "7"},
        {"idemprecuitsa": "5"},
        {"idemprecuitsa": "3"},
        {"idemprecuitsa": "4"}
    ]


def test_filtrar_estaciones_por_provincia():
    estaciones = [
        {"producto": "GNC", "provincia": "Buenos Aires", "latitud": "-34.6037", "longitud": "-58.3816"},
        {"producto": "GNC", "provincia": "Santa Fe", "latitud": "-32.9466", "longitud": "-60.6395"},
        {"producto": "NAFTA", "provincia": "Buenos Aires", "latitud": "-34.6037", "longitud": "-58.3816"},
        {"producto": "GNC", "provincia": "Santa Fe", "latitud": "-33.7456", "longitud": "-61.9688"}
    ]

    assert filtrar_estaciones_por_provincia(estaciones, "Buenos Aires") == [
        {"lat": -34.6037, "lon": -58.3816}
    ]

    assert filtrar_estaciones_por_provincia(estaciones, "Santa Fe") == [
        {"lat": -32.9466, "lon": -60.6395},
        {"lat": -33.7456, "lon": -61.9688}
    ]


def test_contar_marcas_por_provincia():
    estaciones = [
        {"empresa": "YPF"},
        {"empresa": "YPF"},
        {"empresa": "Shell"},
        {"empresa": "Axion"},
        {"empresa": "Shell"}
    ]

    resultado = contar_marcas_por_provincia(estaciones)

    assert resultado == {
        "YPF": 2,
        "Shell": 2,
        "Axion": 1
    }


def test_obtener_precio_mas_barato():
    estaciones = [
        {"provincia": "Santa Fe", "producto": "GNC", "precio": 500, "empresa": "YPF", "localidad": "Rosario"},
        {"provincia": "Santa Fe", "producto": "GNC", "precio": 450, "empresa": "Shell", "localidad": "Santa Fe"},
        {"provincia": "Santa Fe", "producto": "NAFTA", "precio": 700, "empresa": "Axion", "localidad": "Rosario"}
    ]

    resultado = obtener_precio_mas_barato(estaciones, "Santa Fe", "GNC")

    assert resultado == [{
        "combustible": "GNC",
        "provincia": "Santa Fe",
        "empresa": "Shell",
        "localidad": "Santa Fe",
        "precio": 450
    }]


def test_obtener_estacion_barata():
    estaciones = [
        {"provincia": "Santa Fe", "producto": "GNC", "localidad": "Rosario", "precio": 45800, "latitud": "-30.78", "longitud": "-31.45"},
        {"provincia": "Santa Fe", "producto": "GNC", "localidad": "Santa Fe", "precio": 40450, "latitud": "-30.45", "longitud": "-31.77"},
        {"provincia": "Santa Fe", "producto": "Nafta (Super)", "localidad": "Venado Tuerto", "precio": 3050, "latitud": "-30.10", "longitud": "-31.12"},
        {"provincia": "Buenos Aires", "producto": "Nafta (Super)", "localidad": "Santa Fe", "precio": 3500, "latitud": "-30.10", "longitud": "-31.12"}
    ]

    resultado = obtener_estacion_barata(estaciones, "Santa Fe", "GNC")

    assert len(resultado) == 1
    assert resultado[0]["localidad"] == "Santa Fe"
    assert resultado[0]["lat"] == -30.45
    assert resultado[0]["lon"] == -31.77


def test_obtener_campos_unicos():
    estaciones = [
        {"provincia": "Santa Fe", "producto": "GNC", "idempresa": 1},
        {"provincia": "Buenos Aires", "producto": "GNC", "idempresa": 2},
        {"provincia": "Buenos Aires", "producto": "Nafta (Super)", "idempresa": 3},
        {"provincia": "Tucuman", "producto": "Gasoil", "idempresa": 4},
        {"provincia": "Catamarca", "producto": "Nafta (Comun)", "idempresa": 5}
    ]

    assert sorted(obtener_campos_unicos(estaciones, "provincia")) == sorted([
        "Santa Fe", "Buenos Aires", "Tucuman", "Catamarca"
    ])

    assert sorted(obtener_campos_unicos(estaciones, "producto")) == sorted([
        "GNC", "Nafta (Super)", "Gasoil", "Nafta (Comun)"
    ])

    assert sorted(obtener_campos_unicos(estaciones, "idempresa")) == [1, 2, 3, 4, 5]


def test_ordenar_promedios():
    promedios = [
        {"id": 1, "precio_promedio": 10},
        {"id": 2, "precio_promedio": 16},
        {"id": 3, "precio_promedio": 20},
        {"id": 4, "precio_promedio": 4}
    ]

    assert ordenar_promedios(promedios) == [
        {"id": 3, "precio_promedio": 20},
        {"id": 2, "precio_promedio": 16},
        {"id": 1, "precio_promedio": 10},
        {"id": 4, "precio_promedio": 4}
    ]


def test_obtener_10_promedios_altos():
    estaciones = [
        {"idemprecuitsa": 1, "empresa": "YPF", "precio": 150},
        {"idemprecuitsa": 2, "empresa": "Shell", "precio": 200},
        {"idemprecuitsa": 2, "empresa": "Shell", "precio": 100},
        {"idemprecuitsa": 1, "empresa": "YPF", "precio": 120},
        {"idemprecuitsa": 1, "empresa": "YPF", "precio": 50}
    ]

    resultado = obtener_10_promedios_altos(estaciones)

    assert resultado[0]["empresa"] == "Shell"
    assert resultado[0]["precio_promedio"] == 150

    assert resultado[1]["empresa"] == "YPF"
    assert round(resultado[1]["precio_promedio"], 2) == round(320 / 3, 2)