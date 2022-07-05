from django.contrib import admin
from .models import *
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Country)
admin.site.register(Gender)
admin.site.register(Tags)
admin.site.register(Campaign)
admin.site.register(Items)
admin.site.register(Reward)