from gestion_usuarios.models import Hiperparameters_KNN

def create_hiperparameters_KNN(email_id,model_id,type,prime_stack,n_neighbors,weights,
                               algorithm,leaf_size,p,metric):
    hiperparameters_KNN = Hiperparameters_KNN.objects.create(
        email_id = email_id,
        model_id = model_id,
        type = type,
        prime_stack = prime_stack,
        n_neighbors = n_neighbors,
        weights = weights,
        algorithm = algorithm,
        leaf_size = leaf_size,
        p = p,
        metric = metric)
    return hiperparameters_KNN

def get_hiperparameters_KNN(model_id):
    try:
        hiper_KNN = Hiperparameters_KNN.objects.get(model_id=model_id)
        return hiper_KNN
    except Hiperparameters_KNN.DoesNotExist:
        return None

def delete_hiperparameters_KNN(model_id):
    try:
        hiper_KNN = Hiperparameters_KNN.objects.get(model_id=model_id)
        hiper_KNN.delete()
        return True
    except Hiperparameters_KNN.DoesNotExist:
        return False