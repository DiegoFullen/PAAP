from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import os

# ---------------- Paths --------------------------
path_dataset = 'PAAP/dataset/random_forest_examples/Aprobados_Reprobados.csv'
path_model = 'PAAP/models/decision_tree_aprobados_reprobados.pkl'
# ------------------------------------------------

# ---------------- Dataset -----------------------
data = pd.read_csv(path_dataset)
objective = 'Calificacion'

data_encoded = data.copy()
for column in data_encoded.select_dtypes(include='object').columns:
    data_encoded[column] = LabelEncoder().fit_transform(data_encoded[column])

X = data_encoded.drop(columns=[objective])
y = data_encoded[objective]

feature_names = X.columns
class_names = sorted(map(str, set(y)))

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
