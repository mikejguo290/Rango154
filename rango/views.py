from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponse
from rango.models import Category # to access django's model called Category
from rango.models import Page
from rango.forms import CategoryForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from datetime import datetime
from rango.bing_search import run_query # bing search function provided by rango.

def index(request):
	# cookie testing
	request.session.set_test_cookie()
	
	# Request the context of this request
	context = RequestContext(request)
	
	# make a dict to pass to the template engine as its context
	# boldmessage is same as name of python template var we named in index.html
	
	category_list = Category.objects.order_by('-likes')[:5]
	page_list = Page.objects.order_by('-views')[:5]
	
	for category in category_list:
		category.url = category.name.replace(' ','_')

	# dynamically add url attribute to each category in category_list, then pass it on 
	# to index.html
	
	# DON'T do the same for page.url! These are not dynamic. 
	
	context_dict = {'categories':category_list, 'pages': page_list } # so template variable == categories.
	
	# return a rendered response to client
	# shortcuts makes life easier
	# first parameter is the template we need, location is NOT relative.
	
	# get response object early so we can add cookie information
	#response = render_to_response('rango/index.html', context_dict, context)
	
	# Get the number of visits to the site.
	# We use the COOKIES.get() function to obtain the visits cookie.
	# if the cookie exists, the value returned is casted to an integer. Else we default to zero.
	
	#visits = int(request.COOKIES.get('visits',0))
	"""
	if 'last_visit' in request.COOKIES:
		last_visit = request.COOKIES['last_visit']
		# cast the value to a Python date/time object
		last_visit_time = datetime.strptime(last_visit[:-7],"%Y-%m-%d %H:%M:%S")
		
		if (datetime.now() - last_visit_time).seconds > 5:
			# if the same visitor visits this view a day later, only then does the cookie for visitor increment. 
			response.set_cookie('visits', visits+1)
			response.set_cookie('last_visit',datetime.now())
	else:
		# if this was the first visit. create the last_visit to current time
		response.set_cookie('last_visit',datetime.now())
		# cookies will automatically store info as strings.
	"""
	# server side cookies are more secure than client side cookies.
	# only client side cookie is the session id, which is key to all else.
	if request.session.get('last_visit'):
		last_visit_time = request.session['last_visit']
		visits = request.session.get("visits",0)
		
		if(datetime.now() - datetime.strptime(last_visit_time[:-7],"%Y-%m-%d %H:%M:%S")).seconds> 5:
			request.session['visits'] = visits + 1
			request.session['last_visit'] = str(datetime.now())
	else:
		request.session['visits'] = 0 
		request.session['last_visit'] = str(datetime.now())
		
	return render_to_response('rango/index.html',context_dict, context)

def about(request):
	context = RequestContext(request)
	
	context_dict ={}
	
	return render_to_response('rango/about.html', context_dict, context)
	
def food(request):
	#can't return much info without a template. 
	
	# httpResponse can contain html!
	return HttpResponse('Rango says: I love <a href ="/rango/">insects</a>!')
	
def products(request):
	
	context = RequestContext(request)
	context_dict = {}
	return render_to_response('rango/products.html',context_dict,context)

# each category will need to show list of pages associated with it.
def category(request, category_name_url):
	context = RequestContext(request)
	category_name = category_name_url.replace('_',' ') #replace '_' in url with space
	
	
	context_dict = {'category_name': category_name}
	
	try:
		category = Category.objects.get(name = category_name) # get returns just one thing
		pages = Page.objects.filter(category=category) # filter can return a list.
		
		context_dict['pages'] = pages
		context_dict['category'] = category
		
	except Category.DoesNotExist:
		# except when this error pops up. cat does not exist.
		pass
	return render_to_response('rango/category.html',context_dict,context)

#form to add category	
def add_category(request):
	context = RequestContext(request)
	
	# A HTTP post?
	if request.method == "POST":
		form = CategoryForm(request.POST)
		
		# is this a valid form?
		if form.is_valid:
			# save the category to the database.
			form.save(commit = True)
			
			# call index() view and redirect user back to homepage.
			return index(request)
		else:
			#the form contains errors. print these to the terminal.
			print form.errors
	else:
		# if request not POST, must be GET, display form
		form = CategoryForm()
		# display an empty form
		
	return render_to_response('rango/add_category.html',{'form':form},context)
	# context is a form! {'form':form}
	
def register(request):
	# cookie testing
	if request.session.test_cookie_worked():
		print ">>> TEST COOKIE WORKED!"
		request.session.delete_test_cookie()

	context = RequestContext(request)
	
	registered = False
	# boolean variable to tell template about registration outcome. 
	# initially false
	if request.method =='POST':
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)
		if user_form.is_valid() and profile_form.is_valid():
			
			# save the user's form data to db
			user = user_form.save()
			# hash the password with set_password
			user.set_password(user.password)
			user.save()
			
			# we save profile form, don't commit to db immediately, just get var name
			profile = profile_form.save(commit = False)
			# set profile's user association ourselves
			profile.user = user
			
			"""
			# need to install pillow module first 
			if 'picture ' in request.FILES:
				profile.picture = request.FILES['picture']
			"""	
			# now save UserProfile's model instance
			profile.save()
			
			#registration succesfull
			registered = True
			
		else:
			print user_form.errors, profile_form.errors
	else:
		user_form=UserForm()
		profile_form =UserProfileForm()
	
	return render_to_response('rango/register.html',{'user_form':user_form, 'profile_form': profile_form, 'registered': registered},context)
		
def user_login(request):
	context=RequestContext(request)
	
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password'] # get login dets from .POST method
		
		user = authenticate(username = username, password = password) # try to login
		
		if user:
			if user.is_active:
				# if user and is active, then login and redirect back to homepage.
				login(request,user) # why does login() require a request obj?
				return HttpResponseRedirect('/rango/')
			else:
				# in active account - no loggin in! 
				return HttpResponse('Your Rango account is disabled.')
		else:
			#bad login
			print "invalid login details: {0}, {1}".format(username, password)
			return HttpResponse("Invalid login details supplied.")
	# request was not a HTTP Post, so display the login form
	else:
		# with response to GET request, no context_dict, hence empty dict

		return render_to_response('rango/login.html',{},context)
	
@login_required # this is the python decorator - allows me to check login status	
def restricted(request):
	# example of a restricted page
	return HttpResponse(" You can see this since you are logged in!")
	
@login_required
# use the login decorator to ensure only those logged in can view this.
def user_logout(request):
	# since user must be logged in to use this view, 
	# we can just log them out
	
	logout(request)
	
	# Take the user back to homepage
	return HttpResponseRedirect('/rango/')

def search(request):
	context = RequestContext(request)
	result_list =[]
	
	if request.method =='POST':
		query = request.POST['query'].strip()
		
		if query:
			# Run our Bing function to get the results List!
			result_list = run_query(query)
	return render_to_response('rango/search.html', {'result_list': result_list}, context)
	
def history(request):
	"""
	rehash ex3.7
	"""
	context = RequestContext(request)
	
	return render_to_response('rango/history.html',context)	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	