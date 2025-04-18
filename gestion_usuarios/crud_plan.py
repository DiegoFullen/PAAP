from gestion_usuarios.models import Plan

# Crear un nuevo plan
def create_plan(hours, type_plan, email_id):
    plan = Plan.objects.create(
        hours=hours,
        type_plan=type_plan,
        email_id=email_id  # Almacena directamente el correo
    )
    return plan

# Obtener un plan por id
def get_plan(email_id):
    try:
        plan = Plan.objects.get(email_id=email_id)
        return plan
    except Plan.DoesNotExist:
        return None

# Obtener todos los planes
def get_all_plans():
    return Plan.objects.all()

# Actualizar un plan
def update_plan(email_id, **kwargs):
    try:
        plan = Plan.objects.get(email_id=email_id)
        for key, value in kwargs.items():
            setattr(plan, key, value)
        plan.save()
        return plan
    except Plan.DoesNotExist:
        return None
    
# Eliminar un plan
def delete_plan(id):
    try:
        plan = Plan.objects.get(id=id)
        plan.delete()
        return True
    except Plan.DoesNotExist:
        return False