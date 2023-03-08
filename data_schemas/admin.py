from django.contrib import admin

from .models import *

admin.site.register(Schema)
admin.site.register(Column)
admin.site.register(CSVFile)
