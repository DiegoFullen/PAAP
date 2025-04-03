from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import os

# ---------------- Rutas -------------------------

path_dataset = '../algoritmos/dataset/diabetes_dataset.csv'
path_model = '../algoritmos/models/decision_tree_diabetes.pkl'

# ------------------------------------------------

# ---------------- Variables globales ------------
objective = 'Outcome'
# ------------------------------------------------

# ---------------- Dataset -----------------------
    
def prepare_dataset(path_dataset, objective, encode_categorical=True):
    
    #Args:
    #    path_dataset (str): Ruta al archivo CSV del dataset
    #    objective (str): Nombre de la columna objetivo
    #    encode_categorical (bool): Si se deben codificar variables categóricas
    
    #Returns:
    #    tuple: X, y, feature_names, class_names, task_type
    
    # Cargar dataset
    data = pd.read_csv(path_dataset)
    
    # Determinar automáticamente el tipo de tarea (clasificación o regresión)
    if data[objective].dtype == 'object' or len(data[objective].unique()) < 10:
        task_type = 'classification'
    else:
        task_type = 'regression'
    
    # Codificar variables categóricas si es necesario
    data_encoded = data.copy()
    if encode_categorical:
        for column in data_encoded.select_dtypes(include='object').columns:
            data_encoded[column] = LabelEncoder().fit_transform(data_encoded[column])
    
    # Separar características y objetivo
    X = data_encoded.drop(columns=[objective])
    y = data_encoded[objective]
    
    # Obtener nombres de características y clases
    feature_names = X.columns.tolist()
    
    if task_type == 'classification':
        class_names = sorted(map(str, y.unique()))
    else:
        class_names = None
    
    return X, y, feature_names, class_names, task_type

# ---------------- Dividir Datos -----------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# ---------------- Configurar Modelo -------------
clf = DecisionTreeClassifier(
    criterion='entropy',
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    max_leaf_nodes=100,
    min_impurity_decrease=0.01,
    splitter='best',
    random_state=42,
    ccp_alpha=0.01
)

# ---------------- Entrenar Modelo ---------------
clf.fit(X_train, y_train)

# ---------------- Evaluación --------------------
y_pred = clf.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)
print(f'Accuracy: {accuracy * 100:.2f}%')
print(f'Matriz de confusión:\n{cm}')

# ---------------- Visualización -----------------
plt.figure(figsize=(12, 12))
tree.plot_tree(clf, filled=True, feature_names=feature_names, class_names=class_names)
plt.show()

# ---------------- Guardar Modelo ----------------
os.makedirs('Models', exist_ok=True)
joblib.dump(clf, path_model)
