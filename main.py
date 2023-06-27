import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import calendar
from dateutil.parser import parse
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors


###########################################
# Link render https://ferflix.onrender.com
###########################################

app=FastAPI(title='Proyecto Individual_Peliculas',
            description='PI_ML_OPS_DataPT-01',
            version='1.0.1')

@app.get('/')
async def index():
    return {'API TheFercho'}


df = pd.read_csv('./datasets/merged_movies_credits.csv',encoding='utf-8') 
dfML = pd.read_csv('./datasets/dataset_test_ML.csv',encoding='utf-8')


# Cambiamos las fechas de la columna 'release_date' a formato AAAA-mm-dd, ignorando con 'coerce'
# los valores que no cumplen con el criterio para la funcion .to_datetime
df["release_date"] = pd.to_datetime(df['release_date'],errors='coerce')

#class Dia(BaseModel):
 #   dia:str

####################################################################################
# Funcion 1: def cantidad_filmaciones_mes( Mes ): Se ingresa un mes en idioma Español. 
# Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
#  Ejemplo de retorno: X cantidad de películas fueron estrenadas en el mes de X

# => ingresar el siguiente link: http://localhost:8000/cantidad_filmaciones_mes/enero
from dateutil.parser import parse
@app.get('/cantidad_filmaciones_mes/{mes}')
def cantidad_filmaciones_mes(mes):
# Mapear los nombres de los meses en español a los números de mes correspondientes
    meses = {
        'enero': 1,
        'febrero': 2,
        'marzo': 3,
        'abril': 4,
        'mayo': 5,
        'junio': 6,
        'julio': 7,
        'agosto': 8,
        'septiembre': 9,
        'octubre': 10,
        'noviembre': 11,
        'diciembre': 12
    }
# Obtener el número del mes a partir del nombre en español
    mes_numero = meses.get(mes.lower())

    if mes_numero is None:
        raise ValueError('Mes inválido: {}'.format(mes))

    # Filtrar las películas por mes y contar la cantidad
    cantidad = df[df['release_date'].dt.month == mes_numero].shape[0]

    #return f"{cantidad} es la cantidad de películas que fueron estrenadas en el mes de {mes}."
    return {'cantidad_mes':cantidad,'mes':mes}



#####################################################################################
# Funcion 2: def cantidad_filmaciones_dia( Dia ): Se ingresa un día en idioma Español. 
# Debe devolver la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.
# Ejemplo de retorno: X cantidad de películas fueron estrenadas en los días X

# => ingresar el siguiente link: http://localhost:8000/cantidad_filmaciones_dia/lunes
@app.get("/cantidad_filmaciones_dia/{dia}")
async def cantidad_filmaciones_dia(dia):
    # Mapear los nombres de los días en español a los números de día correspondientes
    dias = {
        'lunes': 0,
        'martes': 1,
        'miércoles': 2,
        'jueves': 3,
        'viernes': 4,
        'sábado': 5,
        'domingo': 6
    }

# Obtener el número del día a partir del nombre en español
    dia_numero = dias.get(dia.lower())

    if dia_numero is None:
        raise ValueError('Día inválido: {}'.format(dia))

# Filtrar las películas por día de la semana y contar la cantidad
    cantidad = df[df['release_date'].dt.dayofweek == dia_numero].shape[0]
    return {'cantidad':cantidad, 'dia':dia}
    #return f"{cantidad} es la cantidad de películas que fueron estrenadas en los dias {dia}."

#############################################################################################

# Funcion 3 : def score_titulo( titulo_de_la_filmación ): Se ingresa el título de una filmación esperando como 
# respuesta el título, el año de estreno y el score.
# Ejemplo de retorno: La película X fue estrenada en el año X con un score/popularidad de X

# utilizar el siguiente link => http://localhost:8000/score_titulo_2/toy%story

@app.get("/score_titulo_2/{titulo_de_la_filmacion}")
async def score_titulo_2(titulo_de_la_filmacion:str):
    # Realizamos una búsqueda case insensitive y con coincidencia parcial
    coincidencia = df['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)

    # Filtramos el DataFrame para obtener las filas con coincidencias
    # df_v1[coincidencia]

    # Si hay coincidencias, seleccionamos la primera fila y obtenemos los valores
    if not df[coincidencia].empty:
        row = df[coincidencia].iloc[0]
        #return f"La pelicula {row['title']} fue estrenada en el año {row['release_year']} con un score de {row['vote_average']}"
        
        return {'pelicula':row['title'],'anio':row['release_year'], 'score':row['vote_average']}
    return f"No se encontraron resultados para el título de la filmación: {titulo_de_la_filmacion}"
#############################################################################################

# Funcion 4: def votos_titulo( titulo_de_la_filmación ): Se ingresa el título de una filmación esperando como respuesta el 
# título, la cantidad de votos y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 
# 2000 valoraciones, caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, 
# no se devuelve ningun valor.
# Ejemplo de retorno: La película X fue estrenada en el año X. La misma cuenta con un total de X valoraciones, 
# con un promedio de X.

@app.get('/votos_titulo/{titulo_de_la_filmacion}')
async def votos_titulo(titulo_de_la_filmacion):
    # Realizamos una búsqueda case insensitive y con coincidencia parcial
    matches = df['title'].str.contains(titulo_de_la_filmacion, case=False, na=False)

    # Filtramos el DataFrame para obtener las filas con coincidencias
    df_matches = df[matches]

    # Si hay coincidencias, seleccionamos la primera fila y verificamos el número de valoraciones
    if not df_matches.empty:
        row = df_matches.iloc[0]
        vote_count = row['vote_count']
        if vote_count < 2000:
            return f"La pelicula {row['title']} no obtuvo suficientes valoraciones"
        return {'pelicula':row['title'],'estreno':row['release_year'],'valoraciones':row['vote_count'],'promedio':row['vote_average']}
        #return f"La pelicula {row['title']} fue estrenada en el año {row['release_year']} con un total de {row['vote_count']} valoraciones y un promedio de {row['vote_average']}"
###############################################################################################################

# Funcion 5: def get_actor( nombre_actor ): Se ingresa el nombre de un actor que se encuentre dentro de un dataset 
# debiendo devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que 
# ha participado y el promedio de retorno. La definición no deberá considerar directores.
# Ejemplo de retorno: El actor X ha participado de X cantidad de filmaciones, el mismo ha conseguido un retorno de X 
# con un promedio de X por filmación.

@app.get("/get_actor_2/{nombre_actor}")
async def get_actor_2(nombre_actor):
    actor_films = df[df['cast'].str.contains(nombre_actor, case=False, na=False)]
    cantidad_peliculas = len(actor_films)
    
    # Inicializar el éxito del actor y el total de 'return'
    exito_actor = 0
    total_return = 0
    
    # Calcular el éxito del actor y el total de 'return'
    for _, row in actor_films.iterrows():
        budget = row['budget']
        revenue = row['revenue']
        if revenue != 0:
            return_value = budget / revenue
            exito_actor += return_value
            total_return += 1
    
    # Calcular el promedio de 'return'
    promedio_return = exito_actor / total_return if total_return != 0 else 0
    
    return {'actor':nombre_actor,'cantidad_peliculas':cantidad_peliculas,'retorno_ROI':exito_actor,'promedio_ROI': promedio_return}
    #return f"El actor {nombre_actor} ha participado de {cantidad_peliculas} filmaciones. El mismo ha conseguido un retorno de {round(exito_actor,3)}M con un promedio de {round((promedio_return*100),2)}M por filmación."
########################################################################################

# 
##################################################################################################

# Funcion 6: def get_director( nombre_director ): Se ingresa el nombre de un director que se encuentre dentro 
# de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver:
# => el nombre de cada película con la fecha de lanzamiento, 
# => retorno individual, costo y ganancia de la misma.

@app.get("/get_director_3/{nombre_director}")
async def get_director_3(nombre_director):
    # => el nombre de cada película con la fecha de lanzamiento
    # => para busqueda exacta >> peliculas = df[df['director_name'] == nombre_director][['title', 'release_year']]
    peliculas = df[df['director_name'].str.contains(nombre_director,case=False,na=False)][['title', 'release_date','budget','return']]
    peliculas_lista = peliculas.to_dict('records')
    # => el retorno individual, el éxito del mismo medido a través del retorno.
    exito_director = peliculas['return'].sum()
    costo = peliculas['budget']
    #return {'films':peliculas, 'exito': exito_director, 'costo': costo}
    return {'films':peliculas, 'exito': exito_director, 'costo': costo}

##################################################################################################

# Funcion ML :

#################################################################################################

import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.decomposition import PCA
from sklearn.neighbors import NearestNeighbors

@app.get("/recomendacion_5/{titulo}")
async def recomendacion_5(titulo):
            
   # Obtener el índice de la película que coincide con el título ingresado (case insensitive)
    indices = pd.Series(dfML.index, index=dfML['title'].str.lower()).drop_duplicates()
    titulo_lower = titulo.lower()
    
    if titulo_lower not in indices:
        return "Título no encontrado"
    
    idx = indices[titulo_lower]
    
    # Seleccionar las características relevantes para el algoritmo KNN
    features = ['genres']
    X = dfML[features]
    
    # Convertir las listas en columnas binarias utilizando MultiLabelBinarizer
    mlb = MultiLabelBinarizer()
    encoded_genres = pd.DataFrame(mlb.fit_transform(X['genres']), columns=mlb.classes_, index=X.index)
    
    # Convertir los nombres de características numéricas a cadenas
    numeric_features = X.drop('genres', axis=1)
    numeric_features.columns = numeric_features.columns.astype(str)
    
    # Aplicar PCA para reducir la dimensionalidad
    #El PCA es una técnica de reducción de dimensionalidad que 
    # transforma un conjunto de variables correlacionadas en un conjunto más pequeño de variables no correlacionadas 
    # llamadas componentes principales.
    pca = PCA(n_components=0.6)  # Mantenemos el 60% de la varianza explicada
    encoded_genres_pca = pca.fit_transform(encoded_genres)
    
    # Concatenar las características numéricas y las características transformadas por PCA
    X = pd.concat([numeric_features, pd.DataFrame(encoded_genres_pca)], axis=1)
    
    # Normalizar las características
    X = (X - X.mean()) / X.std()
    
    # Crear una instancia del algoritmo KNN
    knn = NearestNeighbors(n_neighbors=6)  # Consideramos 6 vecinos, incluyendo la película seleccionada
    
    # Resolvemos el siguiente error con la recomendacion de la propia libreria:  
    # Feature names are only supported if all input features have string names, but your input has ['int', 'str'] 
    # as feature name / column name types. If you want feature names to be stored and validated, 
    # you must convert them all to strings, by using: =>>>>> X.columns = X.columns.astype(str)
    #X.columns = X.columns.astype(str)
    
    # Entrenar el modelo KNN
    knn.fit(X)
    
    # Obtener la distancia y los índices de los vecinos más cercanos
    distances, indices = knn.kneighbors(X.iloc[idx].values.reshape(1, -1))
    
    # Obtener los títulos de las películas más similares (excluyendo la película seleccionada)
    similar_movies = dfML['title'].iloc[indices[0][1:6]]
    
    return {'recomendadas':similar_movies}