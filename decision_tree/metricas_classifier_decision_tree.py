import joblib
import pandas as pd
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import precision_recall_curve, average_precision_score
from sklearn.model_selection import learning_curve
from sklearn.model_selection import validation_curve

# Librerias custom 
#from ..clases.preprocesador import Preprocesador

class Preprocesador:
    def __init__(self, ruta_csv, objetivo, test_size=0.3, codificacion="label"):
        self.ruta_csv = ruta_csv
        self.objetivo = objetivo
        self.test_size = test_size
        self.codificacion = codificacion

    def cargar_datos(self):
        data = pd.read_csv(self.ruta_csv)
        return data

    def codificar_datos(self, data):
        data_encoded = data.copy()
        if self.codificacion == "label":
            for column in data_encoded.select_dtypes(include='object').columns:
                data_encoded[column] = LabelEncoder().fit_transform(data_encoded[column])
        elif self.codificacion == "onehot":
            data_encoded = pd.get_dummies(data_encoded)
        return data_encoded

    def dividir_datos(self, data):
        X = data.drop(columns=[self.objetivo])
        y = data[self.objetivo]
        return train_test_split(X, y, test_size=self.test_size, random_state=42)


# ------------------ Cargar Recursos ------------------
# Cargar modelo entrenado
model = joblib.load('../Algoritmos/models/decision_tree_regression.pkl')


# ------------------ Preprocesar Datos ----------------
pre = Preprocesador("../Algoritmos/dataset/random_forest_examples/Aprobados_Reprobados.csv", "Calificacion")
data = pre.cargar_datos() # Cargar datos

data_encoded = pre.codificar_datos(data)
X_train, X_test, y_train, y_test = pre.dividir_datos(data_encoded)

# Codificar dinámicamente
data_encoded = data.copy()
# -----------------------------------------------------------------


# Codificar dinamicamente las columnas categoricas
for column in data_encoded.select_dtypes(include='object').columns:
    data_encoded[column] = LabelEncoder().fit_transform(data_encoded[column])

# Columna objetivo
objetivo = "Calificacion"
X = data_encoded.drop(columns=[objetivo])
y = data_encoded[objetivo]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ---------------------------------------------------------
# ------------------ Matriz de Confusión ------------------
# ---------------------------------------------------------

y_pred = model.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
clases = model.classes_ if hasattr(model, "classes_") else np.unique(y_test)

# Visualizar matriz de confusión
plt.figure(figsize=(8, 6))
sb.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=clases, yticklabels=clases)
plt.xlabel("Predicción")
plt.ylabel("Valor Real")
plt.title("Matriz de Confusión")

# --------------------------------------------------------
# ------------------ Curva ROC-AUC -----------------------
# --------------------------------------------------------

# Probabilidades de predicción
if hasattr(model, "predict_proba"):
    y_score = model.predict_proba(X_test)[:, 1]
    fpr, tpr, thresholds = roc_curve(y_test, y_score)
    auc = roc_auc_score(y_test, y_score)

    # Graficar curva ROC
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {auc:.2f})", color="blue")
    plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random Guessing")
    plt.xlabel("Tasa de Falsos Positivos (FPR)")
    plt.ylabel("Tasa de Verdaderos Positivos (TPR)")
    plt.title("Curva ROC")
    plt.legend(loc="lower right")
    plt.grid()
    
else:
    print("El modelo no soporta predicciones probabilísticas.")


# --------------------------------------------------------
# ------------- Curva de precision recall-----------------
# --------------------------------------------------------

"""
y_scores = model.predict_proba(X_test)[:, 1]
precision, recall, thresholds = precision_recall_curve(y_test, y_scores)
avg_precision = average_precision_score(y_test, y_scores)

plt.figure(figsize=(8, 6))
plt.plot(recall, precision, label=f"AP = {avg_precision:.2f}")
plt.xlabel("Recall", fontsize=14)
plt.ylabel("Precision", fontsize=14)
plt.title("Curva Precisión-Recall", fontsize=16)
plt.legend(loc="best", fontsize=12)
plt.grid(alpha=0.5)
"""

# --------------------------------------------------------
# -------- Grafica de importancia de variables -----------
# --------------------------------------------------------

# Obtener importancias de las características
importances = model.feature_importances_

# Crear un dataframe
feature_importance_df = pd.DataFrame({
    "Feature": X.columns,
    "Importance": importances
}).sort_values(by="Importance", ascending=False)

plt.figure(figsize=(10, 6))
plt.barh(feature_importance_df["Feature"], feature_importance_df["Importance"], color="skyblue")
plt.gca().invert_yaxis()  # Invertir el eje Y para mostrar las más importantes primero
plt.title("Importancia de Variables", fontsize=16)
plt.xlabel("Importancia", fontsize=14)
plt.ylabel("Características", fontsize=14)
plt.grid(axis="x", linestyle="--", alpha=0.7)

# --------------------------------------------------------
# --------------- Curva de aprendizaje -------------------
# --------------------------------------------------------

train_sizes, train_scores, test_scores = learning_curve(
    model, X, y, cv=5, scoring="accuracy", n_jobs=-1, train_sizes=np.linspace(0.1, 1.0, 10)
)

# Promedio y desviación estándar
train_scores_mean = train_scores.mean(axis=1)
train_scores_std = train_scores.std(axis=1)
test_scores_mean = test_scores.mean(axis=1)
test_scores_std = test_scores.std(axis=1)

plt.figure(figsize=(8, 6))
plt.plot(train_sizes, train_scores_mean, 'o-', color="blue", label="Puntaje de Entrenamiento")
plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.2, color="blue")
plt.plot(train_sizes, test_scores_mean, 'o-', color="green", label="Puntaje de Validación")
plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.2, color="green")
plt.title("Curva de Aprendizaje", fontsize=16)
plt.xlabel("Tamaño del Conjunto de Entrenamiento", fontsize=14)
plt.ylabel("Puntaje", fontsize=14)
plt.legend(loc="best", fontsize=12)
plt.grid(alpha=0.5)


# --------------------------------------------------------
# ---------------- Curva de validacion -------------------
# --------------------------------------------------------

# Hiperparametros
param_name = "max_depth"
param_range = np.arange(1, 20)

train_scores, test_scores = validation_curve(
    model, X, y, param_name=param_name, param_range=param_range, cv=5, scoring="accuracy", n_jobs=-1
)

# Promedio y desviación estándar
train_scores_mean = train_scores.mean(axis=1)
train_scores_std = train_scores.std(axis=1)
test_scores_mean = test_scores.mean(axis=1)
test_scores_std = test_scores.std(axis=1)

plt.figure(figsize=(8, 6))
plt.plot(param_range, train_scores_mean, 'o-', color="blue", label="Puntaje de Entrenamiento")
plt.fill_between(param_range, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.2, color="blue")
plt.plot(param_range, test_scores_mean, 'o-', color="green", label="Puntaje de Validación")
plt.fill_between(param_range, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.2, color="green")
plt.title("Curva de Validación", fontsize=16)
plt.xlabel(param_name, fontsize=14)
plt.ylabel("Puntaje", fontsize=14)
plt.legend(loc="best", fontsize=12)
plt.grid(alpha=0.5)


plt.show()