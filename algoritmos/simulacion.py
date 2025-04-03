import ModelMetricService

from pathlib import Path
from sklearn.model_selection import train_test_split

from modelos_ml import (
    DecisionTreeClassification, DecisionTreeRegression,
    RandomForestClassification, RandomForestRegression,
    KNNClassification, KNNRegression,
    prepare_dataset
)

# Clase que simula la llamada desde Django
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
        """
        Inicializa el servicio con el tipo de modelo, el dataset y la columna objetivo.
        
        Args:
            model_type (str): Tipo de modelo a utilizar ('decision_tree_classification', 'knn_regression', etc.).
            dataset_path (str): Ruta al archivo CSV del dataset.
            objective (str): Nombre de la columna objetivo en el dataset.
        """
        if model_type not in self.MODELS:
            raise ValueError(f"Modelo '{model_type}' no soportado. Modelos disponibles: {list(self.MODELS.keys())}")
        
        self.model_class = self.MODELS[model_type]
        self.dataset_path = dataset_path
        self.objective = objective
        self.is_classification = 'classification' in model_type
    
    def execute(self):
        """
        Ejecuta el entrenamiento y evaluación del modelo seleccionado.
        
        Returns:
            dict: Resultados del modelo entrenado.
        """
        # Instanciar el modelo
        model = self.model_class()
        
        # Preparar el dataset usando la función de modelos_ml
        X, y, feature_names, class_names, task_type = prepare_dataset(self.dataset_path, self.objective)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        # Entrenamiento
        model.train(X_train, y_train)
        
        # Evaluación
        if self.is_classification:
            model.evaluate_classification(X_test, y_test)
        else:
            model.evaluate_regression(X_test, y_test)
        
        # Guardar modelo
        model.save_model()
        
        return {
            'model_name': model.model_name,
            'model_path': model.path_model,
            'status': 'Modelo entrenado y guardado con éxito'
        }


# Ejemplo de uso simulando una llamada de Django
def simulate_django_call():
    service = DjangoModelService(
        model_type='decision_tree_classification',
        dataset_path='../algoritmos/dataset/diabetes_dataset.csv',
        objective='Outcome'
    )
    result = service.execute()
    print(result)


# Simular llamada
if __name__ == "__main__":
    simulate_django_call()