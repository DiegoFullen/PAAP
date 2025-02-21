from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import os

# ---------------- Paths --------------------------
path_dataset = 'PAAP/dataset/desicion_tree_examples/consumo_gas.csv'
path_model = 'PAAP/models/decision_tree_consumo_gas.pkl'
# ------------------------------------------------

# ---------------- Dataset -----------------------
data = pd.read_csv(path_dataset)

# Codificar variables categóricas (si aplica)
data_encoded = data.copy()
for column in data_encoded.select_dtypes(include='object').columns:
    data_encoded[column] = LabelEncoder().fit_transform(data_encoded[column])

# Definir variables independientes (X) y dependiente (y)
X = data_encoded.iloc[:, 1:]  # Variables independientes
y = data_encoded.iloc[:, 0]   # Variable dependiente

# ---------------- Dividir Datos -----------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ---------------- Configurar Modelo -------------
reg = DecisionTreeRegressor(
    criterion='squared_error',  # Por defecto en regresión
    max_depth=None,             # Sin límite de profundidad
    min_samples_split=2,        # Default
    min_samples_leaf=1,         # Default
    random_state=42
)

# ---------------- Entrenar Modelo ---------------
reg.fit(X_train, y_train)

# ---------------- Evaluación --------------------
y_pred = reg.predict(X_test)

# Calcular métricas
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)

print(f'Error Cuadrático Medio (MSE): {mse:.2f}')
print(f'Raíz del Error Cuadrático Medio (RMSE): {rmse:.2f}')
print(f'Coeficiente de Determinación (R²): {r2:.2f}')

# ---------------- Visualización -----------------
plt.figure(figsize=(9, 9))  # Ajusta el tamaño si el árbol es grande
tree.plot_tree(
    reg,
    filled=True,
    feature_names=X.columns.tolist(),
    rounded=True
)
plt.show()

# ---------------- Guardar Modelo ----------------
os.makedirs('models', exist_ok=True)
joblib.dump(reg, path_model)
