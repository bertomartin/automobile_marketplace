from django.contrib import admin

from .models import *

admin.site.register(Post)
admin.site.register(Manufacturer)
admin.site.register(BodyType)
admin.site.register(EngineType)
admin.site.register(EngineCapacity)
