from django.contrib import admin
from .models import models

admin.site.register([models.Document, models.DocumentType, models.Help])
