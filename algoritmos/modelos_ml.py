from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, mean_squared_error, r2_score
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from django.http import JsonResponse

import matplotlib.pyplot as plt
import pandas as pd
import joblib
import os
import numpy as np


from django.conf import settings
from gestion_usuarios import crud_dataset

#email = "pruba@prueba.com"
#model_name = "Modelo Prueba"
#dataset_name = "diabetes.csv"

MODELS_PATH = "models/"

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

class ModelosML:
    def __init__(self, dataset, model_path):
        self.dataset_path = dataset.get('path')
        self.model_path = model_path
        print("Dataset path: ", self.dataset_path)
        print("Model path: ", self.dataset_path)

    #DATASET_PATH = os.path.join(settings.MEDIA_ROOT, 'file',email, model_name, dataset_name)
    def _update_model_params(self, model, params):

        """
        Método general para actualizar parámetros en cualquier modelo
        model: Instancia del modelo de scikit-learn
        params: Diccionario de parámetros
        """
        for param_name, param_value in params.items():
            if hasattr(model, param_name):
                # Convertir tipos según lo esperado por scikit-learn
                if param_name in ['n_neighbors', 'max_depth', 'min_samples_split', 
                                  'min_samples_leaf', 'max_leaf_nodes', 'n_estimators']:
                    if param_value and param_value != 'None':
                        param_value = int(param_value)
                    else:
                        continue  # Skip None values for int parameters
                
                elif param_name in ['min_impurity_decrease', 'ccp_alpha', 'p']:
                    if param_value and param_value != 'None':
                        param_value = float(param_value)
                    else:
                        continue
                
                elif param_name in ['bootstrap', 'oob_score']:
                    if isinstance(param_value, str):
                        param_value = param_value.lower() == 'true'
                
                setattr(model, param_name, param_value)
        return model

    def knn_clasificacion(self, **kwargs):
        correction_map = {
            'automatic': 'auto',
            'uniforme': 'uniform',
            'distance': 'distance',
            'minkovski': 'minkowski',
            'balltree': 'ball_tree',
            'kdtree': 'kd_tree',
            'brute-force': 'brute'
        }
        
        # Extraer información del dataset
        dataset_info = kwargs.pop('dataset', {})
        #dataset_path = dataset_info.get('path', DATASET_PATH)
        objective = dataset_info.get('target_column', 'target')
        
        # Crear una instancia del modelo KNN
        model = KNNClassification()

        # Parámetros específicos para KNN
        knn_params = {
            'n_neighbors': kwargs.get('n_neighbors', 5),
            'weights': correction_map.get(kwargs.get('weights', 'uniform'), kwargs.get('weights', 'uniform')),
            'algorithm': correction_map.get(kwargs.get('algorithm', 'auto'), kwargs.get('algorithm', 'auto')),
            'leaf_size': kwargs.get('leaf_size', 30),
            'p': kwargs.get('p', 2),
            'metric': correction_map.get(kwargs.get('metric', 'minkowski'), kwargs.get('metric', 'minkowski'))
        }

        # Actualizar parámetros del modelo
        self._update_model_params(model.model, knn_params)
        
        # Preparar datos y entrenar
        X, y, feature_names, class_names, _ = prepare_dataset(self.dataset_path, objective)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model.train(X_train, y_train)
        
        # Evaluar y devolver resultados
        metrics = self._evaluate_classification_model(model.model, X_test, y_test)
        
        # Guardar modelo con un nombre específico
        model_path = os.path.join(self.model_path, f"{kwargs.get('model_name', 'knn_classification')}.pkl")
        model.path_model = model_path
        model.save_model()
        
        return metrics
    
    def knn_regresion(self, **kwargs):
        # Extraer información del dataset
        dataset_info = kwargs.pop('dataset', {})
        #dataset_path = dataset_info.get('path', self.DATASET_PATH)
        objective = dataset_info.get('target_column', 'target')
        
        # Crear una instancia del modelo KNN Regression
        model = KNNRegression()
        
        # Parámetros específicos para KNN Regression
        knn_params = {
            'n_neighbors': kwargs.get('n_neighbors', 5),
            'weights': kwargs.get('weights', 'uniform'),
            'algorithm': kwargs.get('algorithm', 'auto'),
            'leaf_size': kwargs.get('leaf_size', 30),
            'p': kwargs.get('p', 2),
            'metric': kwargs.get('metric', 'minkowski')
        }
        
        # Actualizar parámetros del modelo
        self._update_model_params(model.model, knn_params)
        
        # Preparar datos y entrenar
        X, y, feature_names, _, _ = prepare_dataset(self.dataset_path, objective)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model.train(X_train, y_train)
        
        # Evaluar y devolver resultados
        metrics = self._evaluate_regression_model(model.model, X_test, y_test)
        
        # Guardar modelo con un nombre específico
        model_path = os.path.join(self.model_path, f"{kwargs.get('model_name', 'knn_regression')}.pkl")
        model.path_model = model_path
        model.save_model()
        
        return metrics
    
    def arbol_clasificacion(self, **kwargs):
        # Extraer información del dataset
        dataset_info = kwargs.pop('dataset', {})
        #dataset_path = dataset_info.get('path', self.DATASET_PATH)
        objective = dataset_info.get('target_column', 'target')
        
        # Crear una instancia del modelo de árbol de decisión
        model = DecisionTreeClassification()
        
        # Parámetros específicos para árboles de decisión
        tree_params = {
            'criterion': kwargs.get('criterion', 'gini'),
            'splitter': kwargs.get('splitter', 'best'),
            'max_depth': kwargs.get('max_depth', None),
            'min_samples_split': kwargs.get('min_samples_split', 2),
            'min_samples_leaf': kwargs.get('min_samples_leaf', 1),
            'max_leaf_nodes': kwargs.get('max_leaf_nodes', None),
            'min_impurity_decrease': kwargs.get('min_impurity_decrease', 0.0),
            'random_state': kwargs.get('random_state', 42),
            'ccp_alpha': kwargs.get('ccp_alpha', 0.0),
            'class_weight': kwargs.get('class_weight', None)
        }
        
        # Actualizar parámetros del modelo
        self._update_model_params(model.model, tree_params)
        
        # Preparar datos y entrenar
        X, y, feature_names, class_names, _ = prepare_dataset(self.dataset_path, objective)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model.train(X_train, y_train)
        
        # Evaluar y devolver resultados
        metrics = self._evaluate_classification_model(model.model, X_test, y_test)
        
        # Guardar modelo con un nombre específico
        model_path = os.path.join(self.model_path, f"{kwargs.get('model_name', 'tree_classification')}.pkl")
        model.path_model = model_path
        model.save_model()
        
        # Crear visualización del árbol si se requiere
        if kwargs.get('visualize', False):
            plt.figure(figsize=(20, 10))
            tree.plot_tree(model.model, feature_names=feature_names, class_names=class_names, filled=True)
            tree_img_path = os.path.join(self.model_path, f"{kwargs.get('model_name', 'tree_classification')}.png")
            plt.savefig(tree_img_path)
            metrics['tree_visualization'] = tree_img_path
        
        return metrics
    
    def arbol_regresion(self, **kwargs):
        # 0 = Squared Error || 1 = Absolute Error
        # 2 = Friedman MSE  || 3 = Poisson
        if (kwargs.get('criterion') == "0"):
            criterion = "squared_error"
        elif (kwargs.get('criterion') == "1"):
            criterion = "absolute_error"
        elif (kwargs.get('criterion') == "2"):
            criterion = "friedman_mse"
        elif (kwargs.get('criterion') == "3"):
            criterion = "poisson"

        # 0 = Mejor || 1 = Aleatorio
        if (kwargs.get('splitter') == "0"):
            splitter = "best"
        elif (kwargs.get('splitter') == "1"):
            splitter = "random"

        # Extraer información del dataset
        dataset_info = kwargs.pop('dataset', {})
        #dataset_path = dataset_info.get('path', self.DATASET_PATH)
        objective = dataset_info.get('target_column', 'target')
        
        # Crear una instancia del modelo de árbol de regresión
        model = DecisionTreeRegression()
        
        # Parámetros específicos para árboles de regresión
        tree_params = {
            'criterion': criterion,
            'splitter': splitter,
            'max_depth': kwargs.get('max_depth', None),
            'min_samples_split': kwargs.get('min_samples_split', 2),
            'min_samples_leaf': kwargs.get('min_samples_leaf', 1),
            'max_leaf_nodes': kwargs.get('max_leaf_nodes', None),
            'min_impurity_decrease': kwargs.get('min_impurity_decrease', 0.0),
            'random_state': kwargs.get('random_state', 42),
            'ccp_alpha': kwargs.get('ccp_alpha', 0.0)
        }
        
        # Actualizar parámetros del modelo
        self._update_model_params(model.model, tree_params)
        
        # Preparar datos y entrenar
        X, y, feature_names, _, _ = prepare_dataset(self.dataset_path, objective)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model.train(X_train, y_train)
        
        # Evaluar y devolver resultados
        metrics = self._evaluate_regression_model(model.model, X_test, y_test)
        
        # Guardar modelo con un nombre específico
        model_path = os.path.join(self.model_path, f"{kwargs.get('model_name', 'tree_regression')}.pkl")
        model.path_model = model_path
        model.save_model()
        
        return metrics
    
    def random_forest_clasificacion(self, **kwargs):
        # Extraer información del dataset
        dataset_info = kwargs.pop('dataset', {})
        #dataset_path = dataset_info.get('path', self.DATASET_PATH)
        objective = dataset_info.get('target_column', 'target')
        
        # Crear una instancia del modelo Random Forest
        model = RandomForestClassification()
        
        # Parámetros específicos para Random Forest
        rf_params = {
            'n_estimators': kwargs.get('n_estimators', 100),
            'criterion': kwargs.get('criterion', 'gini'),
            'max_depth': kwargs.get('max_depth', None),
            'min_samples_split': kwargs.get('min_samples_split', 2),
            'min_samples_leaf': kwargs.get('min_samples_leaf', 1),
            'max_features': kwargs.get('max_features', 'sqrt'),
            'bootstrap': kwargs.get('bootstrap', True),
            'oob_score': kwargs.get('oob_score', False),
            'random_state': kwargs.get('random_state', 42),
            'class_weight': kwargs.get('class_weight', None),
            'max_samples': kwargs.get('max_samples', None)
        }
        
        # Actualizar parámetros del modelo
        self._update_model_params(model.model, rf_params)
        
        # Preparar datos y entrenar
        X, y, feature_names, class_names, _ = prepare_dataset(self.dataset_path, objective)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model.train(X_train, y_train)
        
        # Evaluar y devolver resultados
        metrics = self._evaluate_classification_model(model.model, X_test, y_test)
        
        # Añadir feature importance
        if hasattr(model.model, 'feature_importances_'):
            importances = model.model.feature_importances_
            indices = np.argsort(importances)[::-1]
            feature_importance = {feature_names[i]: float(importances[i]) for i in indices}
            metrics['feature_importance'] = feature_importance
        
        # Guardar modelo con un nombre específico
        model_path = os.path.join(self.model_path, f"{kwargs.get('model_name', 'rf_classification')}.pkl")
        model.path_model = model_path
        model.save_model()
        
        return metrics
    
    def random_forest_regresion(self, **kwargs):
        # Extraer información del dataset
        dataset_info = kwargs.pop('dataset', {})
        #dataset_path = dataset_info.get('path', self.DATASET_PATH)
        objective = dataset_info.get('target_column', 'target')
        
        # Crear una instancia del modelo Random Forest Regression
        model = RandomForestRegression()
        
        # Parámetros específicos para Random Forest Regression
        rf_params = {
            'n_estimators': kwargs.get('n_estimators', 100),
            'criterion': kwargs.get('criterion', 'squared_error'),
            'max_depth': kwargs.get('max_depth', None),
            'min_samples_split': kwargs.get('min_samples_split', 2),
            'min_samples_leaf': kwargs.get('min_samples_leaf', 1),
            'max_features': kwargs.get('max_features', 1.0),
            'bootstrap': kwargs.get('bootstrap', True),
            'oob_score': kwargs.get('oob_score', False),
            'random_state': kwargs.get('random_state', 42),
            'max_samples': kwargs.get('max_samples', None)
        }
        
        # Actualizar parámetros del modelo
        self._update_model_params(model.model, rf_params)
        
        # Preparar datos y entrenar
        X, y, feature_names, _, _ = prepare_dataset(self.dataset_path, objective)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        model.train(X_train, y_train)
        
        # Evaluar y devolver resultados
        metrics = self._evaluate_regression_model(model.model, X_test, y_test)
        
        # Añadir feature importance
        if hasattr(model.model, 'feature_importances_'):
            importances = model.model.feature_importances_
            indices = np.argsort(importances)[::-1]
            feature_importance = {feature_names[i]: float(importances[i]) for i in indices}
            metrics['feature_importance'] = feature_importance
        
        # Guardar modelo con un nombre específico
        model_path = os.path.join(self.model_path, f"{kwargs.get('model_name', 'rf_regression')}.pkl")
        model.path_model = model_path
        model.save_model()
        
        return metrics
    
    def _evaluate_classification_model(self, model, X_test, y_test):
        """Evalúa un modelo de clasificación y devuelve métricas relevantes"""
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        cm = confusion_matrix(y_test, y_pred)
        
        # Calcular precisión, recall y f1-score si es posible
        try:
            from sklearn.metrics import precision_score, recall_score, f1_score, classification_report
            precision = precision_score(y_test, y_pred, average='weighted')
            recall = recall_score(y_test, y_pred, average='weighted')
            f1 = f1_score(y_test, y_pred, average='weighted')
            report = classification_report(y_test, y_pred, output_dict=True)
            
            return {
                "accuracy": float(accuracy),
                "confusion_matrix": cm.tolist(),
                "precision": float(precision),
                "recall": float(recall),
                "f1_score": float(f1),
                "detailed_report": report,
                "predictions_sample": y_pred[:5].tolist()
            }
        except:
            # Si hay error con las métricas avanzadas, retornar solo las básicas
            return {
                "accuracy": float(accuracy),
                "confusion_matrix": cm.tolist(),
                "predictions_sample": y_pred[:5].tolist()
            }
    
    def _evaluate_regression_model(self, model, X_test, y_test):
        """Evalúa un modelo de regresión y devuelve métricas relevantes"""
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        # Calcular métricas adicionales si es posible
        try:
            from sklearn.metrics import mean_absolute_error, explained_variance_score
            mae = mean_absolute_error(y_test, y_pred)
            evs = explained_variance_score(y_test, y_pred)
            rmse = np.sqrt(mse)
            
            return {
                "mse": float(mse),
                "rmse": float(rmse),
                "mae": float(mae),
                "r2_score": float(r2),
                "explained_variance": float(evs),
                "predictions_sample": y_pred[:5].tolist(),
                "actual_sample": y_test[:5].tolist()
            }
        except:
            # Si hay error con las métricas avanzadas, retornar solo las básicas
            return {
                "mse": float(mse),
                "r2_score": float(r2),
                "predictions_sample": y_pred[:5].tolist(),
                "actual_sample": y_test[:5].tolist()
            }

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
    def __init__(self, path_model = MODELS_PATH + 'decision_tree_classification.pkl'):
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
    def __init__(self, path_model = MODELS_PATH + 'decision_tree_regression.pkl'):
        model = DecisionTreeRegressor(
            random_state=42
        )
        super().__init__(model, 'Decision Tree Regression', path_model)

# ---------------- RANDOM FOREST -----------------
class RandomForestClassification(BaseModel):
    def __init__(self, path_model = MODELS_PATH + 'random_forest_classification.pkl'):
        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
            )
        super().__init__(model, 'Random Forest Classification', path_model)

class RandomForestRegression(BaseModel):
    def __init__(self, path_model = MODELS_PATH + 'random_forest_regression.pkl'):
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42
            )
        super().__init__(model, 'Random Forest Regression', path_model)

# ---------------- KNN -----------------
class KNNClassification(BaseModel):
    def __init__(self, path_model = MODELS_PATH + 'knn_classification.pkl'):
        model = KNeighborsClassifier(
            n_neighbors=5
            )
        super().__init__(model, 'KNN Classification', path_model)

class KNNRegression(BaseModel):
    def __init__(self, path_model = MODELS_PATH + 'knn_regression.pkl'):
        model = KNeighborsRegressor(
            n_neighbors=5
            )
        super().__init__(model, 'KNN Regression', path_model)
