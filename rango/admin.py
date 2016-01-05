from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile # new model created to add functionality to auth User

# make Category, Page models available to the admin interface.

admin.site.register(Category)
admin.site.register(Page)
admin.site.register(UserProfile)

