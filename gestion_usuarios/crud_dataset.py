from gestion_usuarios.models import Dataset

# Crear un nuevo dataset
def create_dataset(id_dataset, upload_date, name, size, email_id):
    dataset = Dataset.objects.create(
        id_dataset=id_dataset,
        upload_date=upload_date,
        name=name,
        size=size,
        email_id=email_id 
    )
    return dataset

# Obtener un dataset por id
def get_dataset(id_dataset):
    try:
        dataset = Dataset.objects.get(id_dataset=id_dataset)
        return dataset
    except Dataset.DoesNotExist:
        return None

# Obtener todos los datasets
def get_all_datasets():
    return Dataset.objects.all()

# Actualizar un dataset
def update_dataset(id_dataset, **kwargs):
    try:
        dataset = Dataset.objects.get(id_dataset=id_dataset)
        for key, value in kwargs.items():
            setattr(dataset, key, value)
        dataset.save()
        return dataset
    except Dataset.DoesNotExist:
        return None

# Eliminar un dataset
def delete_dataset(id_dataset):
    try:
        dataset = Dataset.objects.get(id_dataset=id_dataset)
        dataset.delete()
        return True
    except Dataset.DoesNotExist:
        return False

def count_dataset(email_id):
    cantidad = Dataset.objects.filter(email_id=email_id).count()
    return cantidad