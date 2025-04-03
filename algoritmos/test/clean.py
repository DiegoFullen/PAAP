# Primer código (ajustado)
import numpy as np
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
import matplotlib.pyplot as plt

# Cargar dataset
df = pd.read_csv('../algoritmos/test/Datos30k_clean.csv')

# Convertir las recetas en listas
y = df['Recetas'].str.split(', ')

# Binarizar las etiquetas
mlb = MultiLabelBinarizer()
y = mlb.fit_transform(y)

# Contar la frecuencia de cada etiqueta
label_counts = y.sum(axis=0)

# Identificar etiquetas que están en todos los ejemplos
labels_in_all_examples = [i for i, count in enumerate(label_counts) if count == y.shape[0]]

# Mostrar las etiquetas problemáticas
if labels_in_all_examples:
    print("Etiquetas presentes en todos los ejemplos:", labels_in_all_examples)
    print("Nombres de las etiquetas:", mlb.classes_[labels_in_all_examples])
else:
    print("No hay etiquetas presentes en todos los ejemplos.")

# Eliminar estas etiquetas de y (si existen)
if labels_in_all_examples:
    y = np.delete(y, labels_in_all_examples, axis=1)
    mlb.classes_ = np.delete(mlb.classes_, labels_in_all_examples)

# Guardar las etiquetas filtradas para usarlas en el segundo código
filtered_classes = mlb.classes_



# Segundo código (ajustado)
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, hamming_loss

# Cargar dataset limpio
df = pd.read_csv('../algoritmos/test/Datos30k_clean.csv')

# Convertir las recetas en listas
y = df['Recetas'].str.split(', ')

# Reutilizar el MultiLabelBinarizer con las etiquetas filtradas del primer código
mlb = MultiLabelBinarizer(classes=filtered_classes)
y = mlb.fit_transform(y)

# Definir variables predictoras
X = df['Ingredientes']

# Convertir texto a vectores usando TF-IDF
vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
X = vectorizer.fit_transform(X)

# Dividir en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inicializar y entrenar modelo
model = OneVsRestClassifier(LogisticRegression(solver='liblinear', max_iter=1000))
model.fit(X_train, y_train)

# Predecir
y_pred = model.predict(X_test)

# Evaluar
f1 = f1_score(y_test, y_pred, average='micro')
hamming = hamming_loss(y_test, y_pred)
print(f'F1 Score: {f1:.4f}')
print(f'Hamming Loss: {hamming:.4f}')
