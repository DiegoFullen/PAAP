from gestion_usuarios.models import Hiperparameters_Tree

def create_hiperparameters_tree_classify(email_id,model_id,type,prime_stack,criterion,
                                               splitter,max_depth,min_samples_split,
                                               min_leaf_split,max_leaf_nodes,min_impurity_decrease,
                                               max_features,random_state,ccp_alpha,class_weight):
    hiperparameter_tree_class = Hiperparameters_Tree.objects.create(
        email_id = email_id,
        model_id = model_id,
        type = type,
        prime_stack = prime_stack,
        criterion = criterion,
        splitter = splitter,
        max_depth = max_depth,
        min_samples_split = min_samples_split,
        min_leaf_split = min_leaf_split,
        max_leaf_nodes = max_leaf_nodes,
        min_impurity_decrease = min_impurity_decrease,
        max_features = max_features,
        random_state = random_state,
        ccp_alpha = ccp_alpha,
        class_weight = class_weight
    )
    return hiperparameter_tree_class

def create_hiperparameters_tree_regression(email_id, model_id,type,prime_stack,criterion,
                                               splitter,max_depth,min_samples_split,
                                               min_leaf_split,max_leaf_nodes,min_impurity_decrease,
                                               max_features,random_state,ccp_alpha,class_weight):
    hiperparameter_tree_class = Hiperparameters_Tree.objects.create(
        email_id = email_id,
        model_id = model_id,
        type = type,
        prime_stack = prime_stack,
        criterion = criterion,
        splitter = splitter,
        max_depth = max_depth,
        min_samples_split = min_samples_split,
        min_leaf_split = min_leaf_split,
        max_leaf_nodes = max_leaf_nodes,
        min_impurity_decrease = min_impurity_decrease,
        max_features = max_features,
        random_state = random_state,
        ccp_alpha = ccp_alpha,
        class_weight = class_weight
    )
    return hiperparameter_tree_class

def get_hiper_tree(model_id):
    try:
        hiper_tree = Hiperparameters_Tree.objects.get(model_id=model_id)
        return hiper_tree
    except Hiperparameters_Tree.DoesNotExist:
        return None
    
def delete_hiper_tree(model_id):
    try:
       hiper_tree = Hiperparameters_Tree.objects.get(model_id=model_id)
       hiper_tree.delete()
       return True
    except Hiperparameters_Tree.DoesNotExist:
        return False  