from django.shortcuts import render
from django.http import HttpResponse
from promote.models import Promote

# Create your views here.

def all(request):
	promotes = Promote.objects.all()
	context = {
		'promotes':promotes,
	}
	return render(request,'promote/all.html',context)

def new(request):
	if(request.method == 'POST'):
		name = request.POST.get('name')
		startTime = request.POST.get('startTime')
		endTime = request.POST.get('endTime')
		products = request.POST.get('products')
		collections = request.POST.get('collections')
		budget = request.POST.get('budget')
		percentages = request.POST.get('percentages')
		return HttpResonse('hello from post method')
	else:
		return render(request,'promote/new.html')

def settings(request):
	return render(request,'promote/settings.html')

def info(request):
	return render(request,'promote/info.html')

def payment(request):
	return render(request,'promote/payment.html') 

def about(request):
	return render(request,'promote/about.html')

def options(request):
	return render(request,'promote/options.html') 

def promote(request):
	return render(request,'promote/promote.html')

def listings(request):
	promotes = Promote.objects.all() 
	context  = {
		'promotes':promotes,
	} 
	for promote in promotes:
		print(promote.type(), )
	return render(request,'promote/listings.html',context) 
