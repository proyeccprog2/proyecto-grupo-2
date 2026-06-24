from proyecto import obtener_estaciones_unicas, filtrar_estaciones_por_provincia, contar_marcas_por_provincia, obtener_precio_mas_barato

def test_obtener_estaciones_unicas():
    '''Testeamos que la función elimine las empresas repetidas'''
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

    assert obtener_estaciones_unicas(estaciones1) == [{"idemprecuitsa": "1"}, 
                                                     {"idemprecuitsa": "2"}]
    
    assert obtener_estaciones_unicas(estaciones2) == [{"idemprecuitsa": "7"}, 
                                                     {"idemprecuitsa": "5"},
                                                     {"idemprecuitsa": "3"},
                                                     {"idemprecuitsa": "4"}]

def test_filtrar_estaciones_por_provincia():
    '''Testeamos que la función filtre las estaciones que tengan GNC y sean de la provincia seleccionada'''
    estaciones = [{"producto":"GNC", "provincia": "Buenos Aires", "latitud":"-34.6037", "longitud":"-58.3816"},
                   {"producto":"GNC", "provincia": "Santa Fe", "latitud":"-32.9466", "longitud":"-60.6395"},
                   {"producto":"NAFTA", "provincia": "Buenos Aires", "latitud":"-34.6037", "longitud":"-58.3816"},
                   {"producto":"GNC", "provincia": "Santa Fe", "latitud":"-33.7456", "longitud":"-61.9688"}]
    
    assert filtrar_estaciones_por_provincia(estaciones, "Buenos Aires") == [{"lat":-34.6037, "lon":-58.3816}]

    assert filtrar_estaciones_por_provincia(estaciones, "Santa Fe") == [{"lat":-32.9466, "lon":-60.6395},
                                                                         {"lat":-33.7456, "lon":-61.9688}]

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

    assert resultado == {
        "combustible": "GNC",
        "provincia": "Santa Fe",
        "empresa": "Shell",
        "localidad": "Santa Fe",
        "precio": 450
    }