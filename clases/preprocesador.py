from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pandas as pd

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
