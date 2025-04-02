from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
import matplotlib.pyplot as plt
import pandas as pd
import joblib
import os

# ---------------- Rutas -------------------------
DATASET_PATH = '../algoritmos/dataset/dataset.csv'
MODELS_PATH = '../algoritmos/models/'

# ---------------- Dataset -----------------------
def prepare_dataset(path_dataset, objective, encode_categorical=True):
    data = pd.read_csv(path_dataset)
    if data[objective].dtype == 'object' or len(data[objective].unique()) < 10:
        task_type = 'classification'
    else:
        task_type = 'regression'

    data_encoded = data.copy()
    if encode_categorical:
        for column in data_encoded.select_dtypes(include='object').columns:
            data_encoded[column] = LabelEncoder().fit_transform(data_encoded[column])

    X = data_encoded.drop(columns=[objective])
    y = data_encoded[objective]
    feature_names = X.columns.tolist()
    class_names = sorted(map(str, y.unique())) if task_type == 'classification' else None
    
    return X, y, feature_names, class_names, task_type

# Clase base para los modelos
class BaseModel:
    def __init__(self, model, model_name, path_model):
        self.model = model
        self.model_name = model_name
        self.path_model = path_model

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def evaluate_classification(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        print(f'Accuracy: {accuracy * 100:.2f}%')
        print(f'Matriz de confusión:\n{cm}')

    def evaluate_regression(self, X_test, y_test):
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f'Mean Squared Error: {mse:.2f}')
        print(f'R2 Score: {r2:.2f}')
    
    def save_model(self):
        os.makedirs(os.path.dirname(self.path_model), exist_ok=True)
        joblib.dump(self.model, self.path_model)
        print(f'Modelo guardado en {self.path_model}')

# ---------------- ÁRBOLES DE DECISIÓN -----------------
class DecisionTreeClassification(BaseModel):
    def __init__(self, path_model=MODELS_PATH + 'decision_tree_classification.pkl'):
        model = DecisionTreeClassifier(
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
        super().__init__(model, 'Decision Tree Classification', path_model)

class DecisionTreeRegression(BaseModel):
    def __init__(self, path_model=MODELS_PATH + 'decision_tree_regression.pkl'):
        model = DecisionTreeRegressor(
            random_state=42
        )
        super().__init__(model, 'Decision Tree Regression', path_model)

# ---------------- RANDOM FOREST -----------------
class RandomForestClassification(BaseModel):
    def __init__(self, path_model=MODELS_PATH + 'random_forest_classification.pkl'):
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
            )
        super().__init__(model, 'Random Forest Classification', path_model)

class RandomForestRegression(BaseModel):
    def __init__(self, path_model=MODELS_PATH + 'random_forest_regression.pkl'):
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
            )
        super().__init__(model, 'Random Forest Regression', path_model)

# ---------------- KNN -----------------
class KNNClassification(BaseModel):
    def __init__(self, path_model=MODELS_PATH + 'knn_classification.pkl'):
        model = KNeighborsClassifier(
            n_neighbors=5
            )
        super().__init__(model, 'KNN Classification', path_model)

class KNNRegression(BaseModel):
    def __init__(self, path_model=MODELS_PATH + 'knn_regression.pkl'):
        model = KNeighborsRegressor(
            n_neighbors=5
            )
        super().__init__(model, 'KNN Regression', path_model)

# ---------------- EJEMPLO DE USO -----------------
def train_and_evaluate(model_class, path_dataset, objective, classification=True):
    X, y, feature_names, class_names, task_type = prepare_dataset(path_dataset, objective)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = model_class()
    model.train(X_train, y_train)
    
    if classification:
        model.evaluate_classification(X_test, y_test)
    else:
        model.evaluate_regression(X_test, y_test)
    
    model.save_model()
