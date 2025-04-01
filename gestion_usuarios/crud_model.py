from gestion_usuarios.models import Model, Dataset, Hiperparameters_Tree, Hiperparameters_KNN, Hiperparameters_RandomForest
from django.db.models import F
# Crear un nuevo modelo
def create_model(id_model, id_dataset, start_date, finish_date, name, type, type_cr,stack):
    model = Model.objects.create(
        id_model=id_model,
        id_dataset=id_dataset,  # Almacena directamente el ID del dataset
        start_date=start_date,
        finish_date=finish_date,
        name=name,
        type=type,
        type_cr = type_cr,
        primeStack = stack
    )
    return model

# Obtener un modelo por id
def get_model(id_model):
    try:
        model = Model.objects.get(id_model=id_model)
        return model
    except Model.DoesNotExist:
        return None

# Obtener todos los modelos
def get_all_models():
    return Model.objects.all()

#Obtener los modelos especificos del usuario


def get_user_models(email):
    try:
        # Obtener los datasets que coinciden con el email
        datasets = Dataset.objects.filter(email_id=email).values('id_dataset', 'name')
        
        # Crear un diccionario para mapear id_dataset a name
        dataset_map = {ds['id_dataset']: ds['name'] for ds in datasets}

        # Obtener los modelos cuyos id_dataset están en la lista de datasets filtrados
        modelos = Model.objects.filter(id_dataset__in=dataset_map.keys()).values(
            'id_model', 'name', 'type', 'type_cr','id_dataset'
        )

        # Agregar el nombre del dataset a cada modelo y la información adicional
        resultados = []
        for modelo in modelos:
            modelo['name_dataset'] = dataset_map.get(modelo['id_dataset'], 'Desconocido')
            resultados.append(modelo)

        return resultados
    except Exception as e:
        print(f"Error al obtener los modelos: {e}")
        return []

# Actualizar un modelo
def update_model(id_model, **kwargs):
    try:
        model = Model.objects.get(id_model=id_model)
        for key, value in kwargs.items():
            setattr(model, key, value)
        model.save()
        return model
    except Model.DoesNotExist:
        return None
    
# Eliminar un modelo
def delete_model(id_model):
    try:
        model = Model.objects.get(id_model=id_model)
        model.delete()
        return True
    except Model.DoesNotExist:
        return False
    
def count_models(email_id):
    cantidad = Model.objects.filter(email_id=email_id).count()
    return cantidad