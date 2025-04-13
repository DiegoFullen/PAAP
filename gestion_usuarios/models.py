from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, email, username, password, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, password=password, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(primary_key=True, max_length=100)
    username = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=50)
    firstlastname = models.CharField(max_length=50, null=True, blank=True)
    secondlastname = models.CharField(max_length=50, null=True, blank=True)
    email_recover = models.EmailField()
    status = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Dataset(models.Model):
    id_dataset = models.CharField(primary_key=True, max_length=100)
    upload_date = models.DateField()
    name = models.CharField(max_length=100, null=True, blank=True)
    size = models.FloatField()
    email_id = models.EmailField()  # Cambiado de ForeignKey a EmailField

    def __str__(self):
        return self.name

class Model(models.Model):
    id_model = models.CharField(primary_key=True, max_length=100)
    id_dataset = models.CharField(max_length=100)  # Cambiado de ForeignKey a CharField
    email_id = models.EmailField(default='example@example.com')
    start_date = models.DateField(null=True)
    finish_date = models.DateField(null=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=20)
    type_cr = models.IntegerField(default=0)
    primeStack = models.CharField(max_length=70, default='stack')

    def __str__(self):
        return self.name

class Plan(models.Model):
    hours = models.IntegerField()
    type_plan = models.CharField(max_length=50)
    email_id = models.EmailField()  # Cambiado de ForeignKey a EmailField

    def __str__(self):
        return f"{self.type_plan} - {self.hours} horas"

class Temporal(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=128)  # Longitud aumentada para almacenar el hash
    name = models.CharField(max_length=50)
    firstlastname = models.CharField(max_length=50)
    secondlastname = models.CharField(max_length=50)
    email_recover = models.EmailField()
    token = models.CharField(max_length=64)
    created_at = models.DateTimeField(default=timezone.now)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)  # Cifra la contraseña

    def __str__(self):
        return self.email
    
class Hiperparameters_Tree(models.Model):
    email_id = models.EmailField(default='example@example.com')
    model_id = models.CharField(max_length=100)
    type = models.IntegerField() #0 Para Regresión o 1 para Clasificación
    prime_stack = models.CharField(max_length=70)
    #Hiperparametros
    criterion = models.IntegerField()
    splitter = models.IntegerField()
    max_depth = models.FloatField()
    min_samples_split = models.FloatField()
    min_leaf_split = models.FloatField()
    max_leaf_nodes = models.FloatField()
    min_impurity_decrease = models.FloatField()
    max_features = models.FloatField()
    random_state = models.FloatField()
    ccp_alpha = models.FloatField()
    class_weight = models.FloatField()

class Hiperparameters_KNN(models.Model):
    email_id = models.EmailField(default='example@example.com')
    model_id = models.CharField(max_length=100)
    type = models.IntegerField() #0 Para Regresión o 1 para Clasificación
    prime_stack = models.CharField(max_length=70)
    #Hiperparametros
    n_neighbors = models.FloatField()
    weights = models.FloatField()
    algorithm = models.CharField(max_length=15,default='auto' )
    leaf_size = models.FloatField()
    p = models.FloatField()
    metric = models.CharField(max_length=15,default='minkowski' )
    
class Hiperparameters_RandomForest(models.Model):
    email_id = models.EmailField(default='example@example.com')
    model_id = models.CharField(max_length=100)
    type = models.IntegerField() #0 Para Regresión o 1 para Clasificación
    prime_stack = models.CharField(max_length=70)
    #Hiperparametros
    n_estimators = models.FloatField()
    criterion = models.IntegerField()
    max_depth = models.FloatField()
    min_samples_split = models.FloatField()
    min_samples_leaft = models.FloatField()
    max_features = models.CharField(max_length=50)
    bootstrap = models.BooleanField(default=True)
    oob_score = models.IntegerField()
    max_samples = models.FloatField(null=True)
    random_state = models.FloatField()
    class_weight = models.IntegerField()