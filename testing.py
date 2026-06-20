from proyecto import obtener_estaciones_unicas, filtrar_estaciones_por_provincia

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
