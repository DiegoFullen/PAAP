import pandas as pd

df = pd.read_csv('data/archive/nvidia_stock_data.csv')

# -------------- Hiperparametros
n_estimators = 3 
# numero de arboles que el algoritmo construye antes de tomar la votacion maxima
max_features = 3
# numero maximo de caracteristicas que se considera para dividir un nodo
min_sample_leaf = 3
#valor minimo de hojas requeridas para dividir un nodo interno
# -------------- Fin hiperparametros


# -------------- velocidad del modelo
n_jobs = 2 # cuantos procesadores puede usar
random_state = 2 # la salida del modelo es replicable
oob_score = 0.2 # validacion cruzada, datos que se usan para evaluar el rendimiento
# ------------- Fin velocidad
 
