import pandas as pd
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer

# Cargar dataset
df = pd.read_csv('../algoritmos/test/Datos30k.csv')

# Mostrar las primeras filas para inspeccionar
print("Dataset original:")
print(df.head())

# Función para limpiar y normalizar texto
def clean_text(text):
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar caracteres especiales y números (opcional)
    text = re.sub(r'[^\w\s]', '', text)
    # Eliminar espacios adicionales
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# Limpiar la columna de ingredientes
df['Ingredientes'] = df['Ingredientes'].apply(clean_text)

# Limpiar la columna de recetas
df['Recetas'] = df['Recetas'].apply(clean_text)

# Eliminar filas duplicadas
df = df.drop_duplicates()

# Mostrar el dataset después de la limpieza
print("\nDataset después de la limpieza:")
print(df.head())

# Guardar el dataset limpio en un nuevo archivo CSV
df.to_csv('../algoritmos/test/Datos30k_clean.csv', index=False)
print("\nDataset limpio guardado como '../algoritmos/test/Datos30k_clean.csv'.")