import numpy as np
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, hamming_loss

# Cargar dataset
df = pd.read_csv('../algoritmos/test/Datos30k_clean.csv')

# Convertir las recetas en listas
df['Recetas'] = df['Recetas'].str.split(', ')

# Binarizar las etiquetas
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(df['Recetas'])

# Contar la frecuencia de cada etiqueta
label_counts = y.sum(axis=0)

# Identificar etiquetas que están en todos los ejemplos
labels_in_all_examples = [i for i, count in enumerate(label_counts) if count == y.shape[0]]
print("Etiquetas problemáticas:", labels_in_all_examples)

# Nombres de las etiquetas problemáticas
problematic_labels = mlb.classes_[labels_in_all_examples]
print("Nombres de las etiquetas problemáticas:", problematic_labels)

# Eliminar las etiquetas problemáticas directamente del DataFrame
df['Recetas'] = df['Recetas'].apply(lambda recetas: [r for r in recetas if r not in problematic_labels])

# Volver a binarizar las etiquetas con las etiquetas filtradas
y = mlb.fit_transform(df['Recetas'])

# Graficar la nueva distribución de etiquetas
label_counts = y.sum(axis=0)
plt.figure(figsize=(10, 6))
plt.bar(range(len(label_counts)), label_counts)
plt.xlabel('Etiquetas')
plt.ylabel('Frecuencia')
plt.title('Distribución de etiquetas')
plt.xticks(rotation=90)
plt.show()

# Definir variables predictoras
X = df['Ingredientes']

# Convertir texto a vectores usando TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X = vectorizer.fit_transform(X)

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inicializar y entrenar el modelo
model = OneVsRestClassifier(LogisticRegression(solver='liblinear', max_iter=1000))
model.fit(X_train, y_train)

# Predecir
y_pred = model.predict(X_test)

# Evaluar el modelo
f1 = f1_score(y_test, y_pred, average='micro')
hamming = hamming_loss(y_test, y_pred)
print(f'F1 Score: {f1:.4f}')
print(f'Hamming Loss: {hamming:.4f}')
