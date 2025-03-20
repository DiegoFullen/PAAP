from gestion_usuarios.models import Hiperparameters_RandomForest

def create_hiperparameters_RF(email_id,model_id,type,prime_stack,n_estimators,criterion,max_depth,min_samples_split,
                              min_samples_leaft, max_features,bootstrap,oob_score,max_samples,random_state,class_weight):
    hiperparameter_RF = Hiperparameters_RandomForest.objects.create(
        email_id = email_id,
        model_id = model_id,
        type = type,
        prime_stack = prime_stack,
        n_estimators = n_estimators,
        criterion = criterion,
        max_depth = max_depth,
        min_samples_split = min_samples_split,
        min_samples_leaft = min_samples_leaft,
        max_features = max_features,
        bootstrap = bootstrap,
        oob_score = oob_score,
        max_samples = max_samples,
        random_state = random_state,
        class_weight = class_weight
    )
    return hiperparameter_RF

def get_hiperparameters_rf(model_id):
    try:
        hiper_RF = Hiperparameters_RandomForest.objects.get(model_id=model_id)
        return hiper_RF
    except Hiperparameters_RandomForest.DoesNotExist:
        return None
    
def delete_hiperparameters_rf(model_id):
    try:
        hiper_RF = Hiperparameters_RandomForest.objects.get(model_id=model_id)
        hiper_RF.delete()
        return True
    except Hiperparameters_RandomForest.DoesNotExist:
        return False