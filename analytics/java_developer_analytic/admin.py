from django.contrib import admin
from .models import Skills, Demand, GeographyPercent, GeographySalary

admin.site.register(Demand)
admin.site.register(GeographyPercent)
admin.site.register(GeographySalary)
admin.site.register(Skills)
