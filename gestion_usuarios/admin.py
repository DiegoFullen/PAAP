from django.contrib import admin
from .models import User, Dataset, Model, Plan, Temporal

admin.site.register(User)
admin.site.register(Dataset)
admin.site.register(Model)
admin.site.register(Plan)
admin.site.register(Temporal)

