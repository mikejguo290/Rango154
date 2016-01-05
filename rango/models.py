from django.db import models
from django.contrib.auth.models import User # to enable UserForm to use User.

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=128, unique =True)
	views = models.IntegerField(default = 0)
	likes = models.IntegerField(default = 0 )
	
	def __unicode__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length=128)
	url = models.URLField()
	views = models.IntegerField(default = 0)
	
	def __unicode__(self):
		return self.title
		
class UserProfile(models.Model):
	# links user Profile to user.  
	user = models.OneToOneField(User)
	
	# Additional Fields we wish to include
	website = models.URLField(blank = True)
	#picture = models.ImageField(upload_to = 'profile_image',blank = True)
	
	def __unicode__(self):
		return self.user.username
