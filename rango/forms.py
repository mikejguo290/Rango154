from django import forms
from rango.models import Page, Category
from rango.models import UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
	# Doesn't specify parameters
	# can take in POST by a ModelForm
	name= forms.CharField(max_length =128, help_text ="Please enter the category name ")
	views= forms.IntegerField(widget = forms.HiddenInput(), initial =0)
	likes= forms.IntegerField(widget =forms.HiddenInput(), initial = 0)
	
	class Meta:
		# provides an association between form and model.
		model = Category
		
class PageForm(forms.ModelForm):
	title = forms.CharField(max_length =128, help_text="Please enter the title of the page.")
	url = forms.URLField(max_length = 200, help_text ="Please enter the url of the page.")
	views = forms.IntegerField( widget =forms.HiddenInput(),initial = 0)
	
	class Meta:
		model = Page
	
	# here we are specifying the fields shown on Form, even the hidden forms.
	# i guess book used fields () to exclude the foreign key in the Page model.	
	fields = ('title', 'url', 'views')
	
class UserForm(forms.ModelForm):
	username = forms.CharField(help_text = "Please enter a username.")
	email = forms.CharField(help_text ="Please enter your email.")
	password = forms.CharField(widget = forms.PasswordInput(), help_text ="Please enter a password.")
	
	class Meta:
		model = User
		fields = ['username','email','password']
		
class UserProfileForm(forms.ModelForm):
	website = forms.URLField(help_text = "Please enter your website.", required = False)
	#picture = forms.ImageField(help_text = "select a profile image to upload.", required = False)
	class Meta:
		model = UserProfile
		fields = {'website'}#, 'picture'}
	
