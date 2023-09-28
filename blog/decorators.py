from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return redirect('index')
		else:
			return view_func(request, *args, **kwargs)
	
	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):

			group = None
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
			if group in allowed_roles:
				return view_func(request, *args, **kwargs)
			else:
				return HttpResponse("You are not author to view this page ")
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		group = None
		print(f"User group: {group}, {request.user}")
		if request.user.groups.exists():
			group = request.user.groups.all()[0].name
     
		if group == 'customer':
			print(f"User group: {group}, {request.user}")
			return redirect('user')
		
		if group == 'admin':
			print(f"User group: {group}, {request.user}")
			return view_func(request, *args, **kwargs)
			print("Unknown group or no group.")
		return HttpResponse("You are not allow to accses this page. ")
	return wrapper_function
