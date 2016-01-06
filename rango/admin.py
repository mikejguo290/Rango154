from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile # new model created to add functionality to auth User

class PageAdmin(admin.ModelAdmin):
	"""
	Add a new admin object to format Page model output.
	"""
	list_display = ('title', 'category', 'url')

# make Category, Page models available to the admin interface.

admin.site.register(Category)
admin.site.register(Page, PageAdmin) # admin to register Page model together with PageAdmin admin obj
admin.site.register(UserProfile)
	