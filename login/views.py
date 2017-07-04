from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout

import urllib.request
import urllib.parse
import http.cookiejar
import urllib.request

loginsave = login

# Create your views here.
def login(request):
	if request.user.is_authenticated:           
		return HttpResponseRedirect("/nobly/reception/index/")
	return render(request, 'login/login.html')
	
	
def loginsubmit(request):  
	userall = request.POST['userall']
	
	dicttest = {}
	for requestone in request.POST:
		dicttest[requestone] = request.POST[requestone]

	user = authenticate(username='john', password=userall)
	if user is not None:
		loginsave(request, user)
		return HttpResponseRedirect("/nobly/reception/index/")
	else:
		return render(request, 'login/login.html')

		
def loginout(request):
	logout(request)
	return HttpResponseRedirect('/nobly/login/')