from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import joblib
from sklearn.metrics import confusion_matrix, roc_curve, roc_auc_score, precision_recall_curve, average_precision_score
from sklearn.model_selection import learning_curve, validation_curve
import io
import base64
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class ModelMetricsService:
    """
    Servicio para generar y visualizar métricas de modelos de ML.
    """
    
    def __init__(self, model_path, dataset_path, objective):
        """
        Inicializa el servicio de métricas.
        
        Args:
            model_path (str): Ruta al modelo guardado (.pkl)
            dataset_path (str): Ruta al archivo CSV del dataset
            objective (str): Nombre de la columna objetivo
        """
        self.model_path = model_path
        self.dataset_path = dataset_path
        self.objective = objective
        self.model = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.figures = {}
    
    def load_model(self):
        """Carga el modelo guardado."""
        try:
            self.model = joblib.load(self.model_path)
            return True
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            return False
    
    def prepare_data(self):
        """Prepara los datos para las métricas."""
        try:
            # Cargar datos
            data = pd.read_csv(self.dataset_path)
            
            # Codificar variables categóricas
            data_encoded = data.copy()
            for column in data_encoded.select_dtypes(include='object').columns:
                data_encoded[column] = LabelEncoder().fit_transform(data_encoded[column])
            
            # Dividir en características y objetivo
            X = data_encoded.drop(columns=[self.objective])
            y = data_encoded[self.objective]
            
            # División en entrenamiento y prueba
            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                X, y, test_size=0.3, random_state=42
            )
            
            # Para algunas métricas necesitamos todo el conjunto
            self.X = X
            self.y = y
            
            return True
        except Exception as e:
            print(f"Error al preparar los datos: {e}")
            return False
    
    def get_confusion_matrix(self):
        """Genera la matriz de confusión."""
        try:
            y_pred = self.model.predict(self.X_test)
            cm = confusion_matrix(self.y_test, y_pred)
            
            # Determinar las clases
            clases = self.model.classes_ if hasattr(self.model, "classes_") else np.unique(self.y_test)
            
            # Crear la figura
            plt.figure(figsize=(8, 6))
            sb.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=clases, yticklabels=clases)
            plt.xlabel("Predicción")
            plt.ylabel("Valor Real")
            plt.title("Matriz de Confusión")
            
            # Guardar la figura para devolverla
            self.figures['confusion_matrix'] = self._save_figure()
            return True
        except Exception as e:
            print(f"Error al generar la matriz de confusión: {e}")
            return False
    
    def get_roc_curve(self):
        """Genera la curva ROC."""
        try:
            # Verificar si el modelo puede generar probabilidades
            if hasattr(self.model, "predict_proba"):
                y_score = self.model.predict_proba(self.X_test)[:, 1]
                fpr, tpr, thresholds = roc_curve(self.y_test, y_score)
                auc = roc_auc_score(self.y_test, y_score)
                
                # Graficar
                plt.figure(figsize=(8, 6))
                plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {auc:.2f})", color="blue")
                plt.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Random Guessing")
                plt.xlabel("Tasa de Falsos Positivos (FPR)")
                plt.ylabel("Tasa de Verdaderos Positivos (TPR)")
                plt.title("Curva ROC")
                plt.legend(loc="lower right")
                plt.grid()
                
                # Guardar la figura
                self.figures['roc_curve'] = self._save_figure()
                return True
            else:
                print("El modelo no soporta predicciones probabilísticas.")
                return False
        except Exception as e:
            print(f"Error al generar la curva ROC: {e}")
            return False
    
    def get_precision_recall_curve(self):
        """Genera la curva de precisión-recall."""
        try:
            if hasattr(self.model, "predict_proba"):
                y_scores = self.model.predict_proba(self.X_test)[:, 1]
                precision, recall, thresholds = precision_recall_curve(self.y_test, y_scores)
                avg_precision = average_precision_score(self.y_test, y_scores)
                
                plt.figure(figsize=(8, 6))
                plt.plot(recall, precision, label=f"AP = {avg_precision:.2f}")
                plt.xlabel("Recall", fontsize=14)
                plt.ylabel("Precision", fontsize=14)
                plt.title("Curva Precisión-Recall", fontsize=16)
                plt.legend(loc="best", fontsize=12)
                plt.grid(alpha=0.5)
                
                # Guardar la figura
                self.figures['precision_recall_curve'] = self._save_figure()
                return True
            else:
                print("El modelo no soporta predicciones probabilísticas.")
                return False
        except Exception as e:
            print(f"Error al generar la curva de precisión-recall: {e}")
            return False
    
    def get_feature_importance(self):
        """Genera el gráfico de importancia de características."""
        try:
            if hasattr(self.model, "feature_importances_"):
                # Obtener importancias
                importances = self.model.feature_importances_
                
                # Crear dataframe
                feature_importance_df = pd.DataFrame({
                    "Feature": self.X.columns,
                    "Importance": importances
                }).sort_values(by="Importance", ascending=False)
                
                # Graficar
                plt.figure(figsize=(10, 6))
                plt.barh(feature_importance_df["Feature"], feature_importance_df["Importance"], color="skyblue")
                plt.gca().invert_yaxis()
                plt.title("Importancia de Variables", fontsize=16)
                plt.xlabel("Importancia", fontsize=14)
                plt.ylabel("Características", fontsize=14)
                plt.grid(axis="x", linestyle="--", alpha=0.7)
                
                # Guardar figura
                self.figures['feature_importance'] = self._save_figure()
                return True
            else:
                print("El modelo no proporciona importancia de características.")
                return False
        except Exception as e:
            print(f"Error al generar el gráfico de importancia: {e}")
            return False
    
    def get_learning_curve(self):
        """Genera la curva de aprendizaje."""
        try:
            train_sizes, train_scores, test_scores = learning_curve(
                self.model, self.X, self.y, cv=5, 
                scoring="accuracy", n_jobs=-1, 
                train_sizes=np.linspace(0.1, 1.0, 10)
            )
            
            # Calcular promedios y desviaciones
            train_scores_mean = train_scores.mean(axis=1)
            train_scores_std = train_scores.std(axis=1)
            test_scores_mean = test_scores.mean(axis=1)
            test_scores_std = test_scores.std(axis=1)
            
            # Graficar
            plt.figure(figsize=(8, 6))
            plt.plot(train_sizes, train_scores_mean, 'o-', color="blue", label="Puntaje de Entrenamiento")
            plt.fill_between(
                train_sizes, 
                train_scores_mean - train_scores_std, 
                train_scores_mean + train_scores_std, 
                alpha=0.2, color="blue"
            )
            plt.plot(train_sizes, test_scores_mean, 'o-', color="green", label="Puntaje de Validación")
            plt.fill_between(
                train_sizes, 
                test_scores_mean - test_scores_std, 
                test_scores_mean + test_scores_std, 
                alpha=0.2, color="green"
            )
            plt.title("Curva de Aprendizaje", fontsize=16)
            plt.xlabel("Tamaño del Conjunto de Entrenamiento", fontsize=14)
            plt.ylabel("Puntaje", fontsize=14)
            plt.legend(loc="best", fontsize=12)
            plt.grid(alpha=0.5)
            
            # Guardar figura
            self.figures['learning_curve'] = self._save_figure()
            return True
        except Exception as e:
            print(f"Error al generar la curva de aprendizaje: {e}")
            return False
    
    def get_validation_curve(self, param_name="max_depth", param_range=None):
        """
        Genera la curva de validación para un hiperparámetro.
        
        Args:
            param_name (str): Nombre del hiperparámetro a evaluar
            param_range (list): Rango de valores para el hiperparámetro
        """
        try:
            if param_range is None:
                param_range = np.arange(1, 20)
            
            train_scores, test_scores = validation_curve(
                self.model, self.X, self.y, 
                param_name=param_name, param_range=param_range, 
                cv=5, scoring="accuracy", n_jobs=-1
            )
            
            # Calcular promedios y desviaciones
            train_scores_mean = train_scores.mean(axis=1)
            train_scores_std = train_scores.std(axis=1)
            test_scores_mean = test_scores.mean(axis=1)
            test_scores_std = test_scores.std(axis=1)
            
            # Graficar
            plt.figure(figsize=(8, 6))
            plt.plot(param_range, train_scores_mean, 'o-', color="blue", label="Puntaje de Entrenamiento")
            plt.fill_between(
                param_range, 
                train_scores_mean - train_scores_std, 
                train_scores_mean + train_scores_std, 
                alpha=0.2, color="blue"
            )
            plt.plot(param_range, test_scores_mean, 'o-', color="green", label="Puntaje de Validación")
            plt.fill_between(
                param_range, 
                test_scores_mean - test_scores_std, 
                test_scores_mean + test_scores_std, 
                alpha=0.2, color="green"
            )
            plt.title("Curva de Validación", fontsize=16)
            plt.xlabel(param_name, fontsize=14)
            plt.ylabel("Puntaje", fontsize=14)
            plt.legend(loc="best", fontsize=12)
            plt.grid(alpha=0.5)
            
            # Guardar figura
            self.figures['validation_curve'] = self._save_figure()
            return True
        except Exception as e:
            print(f"Error al generar la curva de validación: {e}")
            return False
    
    def _save_figure(self):
        """Guarda una figura en formato base64 para mostrar en web."""
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        buf.seek(0)
        img_str = base64.b64encode(buf.read()).decode('utf-8')
        return img_str
    
    def generate_all_metrics(self):
        """Genera todas las métricas disponibles."""
        if not self.load_model():
            return {"error": "No se pudo cargar el modelo."}
        
        if not self.prepare_data():
            return {"error": "No se pudieron preparar los datos."}
        
        # Generar todas las métricas
        metrics_status = {
            "confusion_matrix": self.get_confusion_matrix(),
            "roc_curve": self.get_roc_curve(),
            "precision_recall": self.get_precision_recall_curve(),
            "feature_importance": self.get_feature_importance(),
            "learning_curve": self.get_learning_curve(),
            "validation_curve": self.get_validation_curve()
        }
        
        # Filtrar las métricas que no se pudieron generar
        available_metrics = {k: v for k, v in self.figures.items() if k in metrics_status and metrics_status[k]}
        
        return {
            "status": "success",
            "metrics": list(available_metrics.keys()),
            "figures": available_metrics
        }


# Ejemplo de uso simulando llamada de Django
def simulate_metrics_call():
    service = ModelMetricsService(
        model_path='../algoritmos/models/decision_tree_classification.pkl',
        dataset_path='../algoritmos/dataset/diabetes_dataset.csv',
        objective='Outcome'
    )
    
    result = service.generate_all_metrics()
    
    # En una aplicación real, estas imágenes se enviarían a la plantilla
    if "error" not in result:
        print(f"Métricas generadas: {result['metrics']}")
        # En Django, los datos base64 se enviarían a la plantilla
        # Para ver una imagen, descomentar la siguiente línea:
        # print(f"Ejemplo de datos de imagen: {result['figures']['confusion_matrix'][:50]}...")
    else:
        print(f"Error: {result['error']}")
    
    return result


# Integración con el servicio de modelos
from modelos_ml import (
    DecisionTreeClassification, DecisionTreeRegression,
    RandomForestClassification, RandomForestRegression,
    KNNClassification, KNNRegression,
    prepare_dataset
)
from sklearn.model_selection import train_test_split

class DjangoModelService:
    
    MODELS = {
        'decision_tree_classification': DecisionTreeClassification,
        'decision_tree_regression': DecisionTreeRegression,
        'random_forest_classification': RandomForestClassification,
        'random_forest_regression': RandomForestRegression,
        'knn_classification': KNNClassification,
        'knn_regression': KNNRegression,
    }
    
    def __init__(self, model_type: str, dataset_path: str, objective: str):
        if model_type not in self.MODELS:
            raise ValueError(f"Modelo '{model_type}' no soportado. Modelos disponibles: {list(self.MODELS.keys())}")
        
        self.model_class = self.MODELS[model_type]
        self.dataset_path = dataset_path
        self.objective = objective
        self.is_classification = 'classification' in model_type
    
    def execute(self):
        # Instanciar el modelo
        model = self.model_class()
        
        # Preparar el dataset
        X, y, feature_names, class_names, task_type = prepare_dataset(self.dataset_path, self.objective)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Entrenar modelo
        model.train(X_train, y_train)
        
        # Evaluar modelo
        if self.is_classification:
            model.evaluate_classification(X_test, y_test)
        else:
            model.evaluate_regression(X_test, y_test)
        
        # Guardar modelo
        model.save_model()
        
        # Generar métricas
        metrics_service = ModelMetricsService(
            model_path=model.path_model,
            dataset_path=self.dataset_path,
            objective=self.objective
        )
        metrics_result = metrics_service.generate_all_metrics()
        
        return {
            'model_name': model.model_name,
            'model_path': model.path_model,
            'status': 'Modelo entrenado y guardado con éxito',
            'metrics': metrics_result
        }


# Ejemplo completo
def simulate_full_pipeline():
    # Entrenar modelo y generar métricas
    service = DjangoModelService(
        model_type='decision_tree_classification',
        dataset_path='../algoritmos/dataset/diabetes_dataset.csv',
        objective='Outcome'
    )
    
    result = service.execute()
    
    print(f"Modelo: {result['model_name']}")
    print(f"Guardado en: {result['model_path']}")
    print(f"Estado: {result['status']}")
    
    if 'metrics' in result and 'metrics' in result['metrics']:
        print(f"Métricas generadas: {result['metrics']['metrics']}")
    
    return result


# Para ejecutar solo la parte de métricas
if __name__ == "__main__":
    # simulate_metrics_call()  # Para probar solo las métricas
    simulate_full_pipeline()   # Para probar el pipeline completo