

# **Proyecto PI MLOps Recomendación películas.** :heavy_check_mark:

[demo youtube](https://youtu.be/02D6bs30Tkk)


## **El proyecto:** Empezaste a trabajar como **`Data Scientist`** en una start-up que provee servicios de agregación de plataformas de streaming.
- Crearemos un modelo de ML que soluciona un problema de negocio: un sistema de recomendación que aún no ha sido puesto en marcha! 
- Para ello debemos realizar un proceso de **ETL + EDA** en los 2 archivos.csv, para luego consultar a traves de una **API**, información relacionada a la propuesta del proyecto.


## **ETL**:

- La **limpieza y transformación** de los datos proviene de 2 archivos: movies_dataset.csv y credits.csv. La info de éste último fue incluída a traves de un merge, ya que por tamaño del mismo por fué posible incluir en el repo.

- Algunos campos, como **`belongs_to_collection`**, **`production_companies`** y otros están anidados, esto es o bien tienen un diccionario o una lista como valores en cada fila, y por ello fué necesario desanidarlos para poder  y unirlos al dataset de nuevo hacer alguna de las consultas de la API! O bien buscar la manera de acceder a esos datos sin desanidarlos.

- Los valores nulos de los campos **`revenue`**, **`budget`** fueron rellenados por el número **`0`**.
    
- Los valores nulos del campo **`release date`** fueron eliminados.

- Las fechas, se modificaron al formato **`AAAA-mm-dd`**, además se creó la columna **`release_year`** donde se extrae el año de la fecha de estreno.

- Se crea la columna con el retorno de inversión, llamada **`return`** con los campos **`revenue`** y **`budget`**, dividiendo estas dos últimas **`revenue / budget`**, cuando no hay datos disponibles para calcularlo, toma el valor **`0`**.

- Se eliminan las columnas que no serán utilizadas, **`video`**,**`imdb_id`**,**`adult`**,**`original_title`**,**`poster_path`** y **`homepage`**.
El análisis se encuentra en los archivos [ETL_Movies.csv](https://github.com/TheFercho/movie-recommendation/blob/master/ipynb/ETL_Movies.ipynb) y [ETL_credits.csv](https://github.com/TheFercho/movie-recommendation/blob/master/ipynb/ETL_credits.ipynb)   

## **EDA**:

- Una vez realizado el ETL, se procede a realizar el Análisis exploratorio de datos para sacar conclusiones de la información relevante para el proyecto solicitado y descubrir si hay algún patrón interesante que valga la pena explorar en un análisis posterior. 
- Entre las herramientas de análisis utilizadas, se muestran **wordClouds**, por ejemplo.
- Las nubes de palabras dan una buena idea de cuáles palabras son más frecuentes en los títulos
     
- El **análisis** se encuentra en el [EDA.ipynb](https://github.com/TheFercho/movie-recommendation/blob/master/EDA.ipynb)



## **Guía de uso**:
- Las librerías utilizadas en el proyecto se encuentran en el archivo [requirements.txt](https://github.com/TheFercho/movie-recommendation/blob/master/requirements.txt)


## **Características y funcionalidades**: 

- **Desarrollo API**:   Se utiliza el framework **FastAPI** para disponibilizar los datos de la empresa, **uvicorn** para el desarrollo a nivel local y **Render** para acceder a nuestra API desde 

- Se crean **6 funciones** para los endpoints que se consumirán en la API:
  
- def **cantidad_filmaciones_mes( *`Mes`* )**:
    Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.

- def **cantidad_filmaciones_dia( *`Dia`* )**:
    Se ingresa un día en idioma Español. Debe devolver la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.


- def **score_titulo( *`titulo_de_la_filmación`* )**:
    Se ingresa el título de una filmación esperando como respuesta el título, el año de estreno y el score.
    

- def **votos_titulo( *`titulo_de_la_filmación`* )**:
    Se ingresa el título de una filmación esperando como respuesta el título, la cantidad de votos y el valor promedio de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que por ende, no se devuelve ningun valor.
    

- def **get_actor( *`nombre_actor`* )**:
    Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha participado y el promedio de retorno. **La definición no deberá considerar directores.**
    

- def **get_director( *`nombre_director`* )**:
    Se ingresa el nombre de un director que se encuentre dentro de un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, deberá devolver el nombre de cada película con la fecha de lanzamiento, retorno individual, costo y ganancia de la misma.

## **Machine learning**:

- def **recomendacion( *`titulo`* )**:
    Se ingresa el nombre de una película y te recomienda las similares en una lista de 5 valores.

- Una vez que toda la data es consumible por la API, está lista para consumir por los departamentos de Analytics y Machine Learning, y nuestro EDA 
nos permite entender bien los datos a los que tenemos acceso, es hora de entrenar nuestro modelo de machine learning para armar un sistema de 
recomendación de películas.

## **Fuente de datos**: 

- [Dataset](https://drive.google.com/drive/folders/1nvSjC2JWUH48o3pb8xlKofi8SNHuNWeu): Carpeta con los 2 archivos con datos que requieren ser procesados (movies_dataset.csv y credits.csv), tengan en cuenta que hay datos que estan anidados (un diccionario o una lista como valores en la fila).

- [Diccionario de datos](https://docs.google.com/spreadsheets/d/1QkHH5er-74Bpk122tJxy_0D49pJMIwKLurByOfmxzho/edit#gid=0): Diccionario con algunas descripciones de las columnas disponibles en el dataset.

- **Links**:
    https://ferflix.onrender.com/docs **`Deployment`**:

    https://fastapi.tiangolo.com/es/#requisitos 

    https://github.com/TheFercho/movie-recommendation 

    https://www.uvicorn.org/
  
    YouTube https://youtu.be/02D6bs30Tkk

       
 
