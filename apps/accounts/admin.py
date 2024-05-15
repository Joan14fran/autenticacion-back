from django.contrib import admin
from .models import User, OneTimePasssword

# Register your models here.
admin.site.register(User)
admin.site.register(OneTimePasssword)
