
import seaborn as sb
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score

class MetricasGlobal:
    @staticmethod
    def matriz_confusion(y_test, y_pred, clases):
        cm = confusion_matrix(y_test, y_pred)
        return cm

    @staticmethod
    def curva_roc(y_test, y_score):
        fpr, tpr, _ = roc_curve(y_test, y_score)
        auc = roc_auc_score(y_test, y_score)
        return fpr, tpr, auc