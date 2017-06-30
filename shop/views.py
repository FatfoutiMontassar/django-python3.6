# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth import authenticate

from django.contrib.auth import login as auth_login , logout as auth_logout

from django.shortcuts import render , redirect

from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User

from django.http import HttpResponse , Http404

from .models import Product, Store, Contact

from .forms import StoreForm, ProductForm , ContactForm

from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator

# Create your views here.
def categories(request,idC,idP):
	if(int(idC) > 6 or int(idC) < 1 ):
		return redirect('/shop')
	categories = [ "Vétement et accessoires" , "Bijoux" , "Founiture créatives" , "Mariages" , "Maison" , "Enfant et bébé" ]
	products = Product.objects.all().filter(categorie=categories[int(idC)-1]).order_by("-created_at")[:180]
	#print categories[int(idC)-1]
	pages = Paginator(products,9)
	intList = list(range(1,((products.count()+8)/9)+1))
	idList = []
	for id in intList:
		idList.append(str(id))

	verifiedId = idP
	if( int(idP) > ((products.count()+8)/9) or int(idP) < 1 ):
		verifiedId = 1
	context = {
		'page':pages.page(verifiedId),
		'pageId':verifiedId,
		'idList':idList,
		'idC':idC,
		'nP':products.count()
	}
	#print products.count()
	return render(request,'categories.html',context)

def discovermore(request,id):
	print "hello from page!"
	products = Product.objects.all().order_by("-created_at")[:180]
	pages = Paginator(products,9)
	#print "number of pages : " + str((products.count()+8)/9)
	intList = list(range(1,((products.count()+8)/9)+1))
	verifiedId = id

	idList = []
	for i in intList:
		idList.append(str(i))

	if( int(id) > ((products.count()+8)/9) or int(id) < 1 ):
		verifiedId = 1

	context = {
		'nPages':pages.num_pages,
		'page':pages.page(verifiedId),
		'pageId':verifiedId,
		'idList':idList,
	}
	#return render(request,'discover',context)
	return render(request , 'discover.html' ,context)

def discover(request):
	#print "hello from discover!"
	products = Product.objects.all().order_by("-created_at")[:180]
	pages = Paginator(products,9)
	idList = list(range(1,((products.count()+8)/9)+1))
	context = {
		'nPages':pages.num_pages,
		'page':pages.page(1),
		'pageId':1,
		'idList':idList,
	}
	return render(request,'discover.html' ,context)

def product_details(request,id):
	product = Product.objects.get(id=id)
	context = {
		'product':product
	}
	return render(request,'product_details.html',context)

def store_details(request,id):
	store = Store.objects.get(id=id)
	context = {
		'store':store,
	}
	return render(request,'store_details.html',context)

def product_create(request,id):
	if not request.user.is_authenticated():
		raise Http404

	if(not request.user.id == Store.objects.get(id=id).user.id):
		raise Http404
	else:
		if(request.method == 'POST'):
			form = ProductForm(request.POST or None,request.FILES or None)
			print form.errors
			if form.is_valid():
				instance = form.save(commit=False)
				store = Store.objects.get(id=id)
				#print instance
				instance.store = store
				instance.isActive = False
				instance.save()
			else:
				print "Error !!"
			return redirect('/shop/details/'+id)
		else:
			store = Store.objects.get(id=id)
			form = ProductForm()
			context = {
				'form':form,
				'store':store,
			}
			#print store.name
			return render(request,'product_form.html',context)

def store_create(request):
	if not request.user.is_authenticated():
		raise Http404
	else:
		if(request.method == 'POST'):
			form = StoreForm(request.POST or None,request.FILES or None)
			#print form.errors
			if form.is_valid():
				instance = form.save(commit=False)
				if(Store.objects.filter(name=instance.name).filter(user=request.user).exists()):
					form = StoreForm()
					context = {
						'form':form,
						'error_message':"Error !! you have already created a store with the same name",
					}
					return render(request , 'store_form.html' ,context)
				else:
					instance.user = request.user
					instance.save()
					return redirect('/shop/stores')
			else:
				form = StoreForm()
				context = {
					'form':form,
					'error_message':"Error !! form is not valid",
				}
				return render(request , 'store_form.html' ,context)
		else:
			form = StoreForm()
			context = {
				'form':form,
			}
			return render(request , 'store_form.html' ,context)

def storesView(request):
	stores = Store.objects.all()[:18]

	context = {
		'stores':stores
	}
	return render(request , 'stores.html' ,context)

def product(request,id):
	product = Product.objects.get(id=id)

	context = {
		'product':product
	}
	return render(request , 'product.html' ,context)
# the trick is to use email as username and username as email :p (it will work perfecty as us username is unique)
def register(request):
	if(request.method == 'POST'):
		#uname = request.POST['uname']
		email = request.POST['email']
		#fname = request.POST['fname']
		#lname = request.POST['lname']
		password = request.POST['password']
		confirmPassword = request.POST['confirmPassword']

		if(password == confirmPassword):
			print "password == confirmPassword"
			if(User.objects.filter(username=email).exists()):
				print("Error , acout alreasy exists")
			else:
				user = User.objects.create_user(username=email,password=password)
				user.save()
				user = authenticate(username=email,password=password)
				if user is not None:
					if user.is_active:
						auth_login(request,user)
						return redirect('/shop')
				else:
					return redirect('/shop/login')
		else:
			print "password and confirmation password dont match !"
		'''
		else:
			return redirect('/shop')
		user = User.objects.create_user(username=uname,email=email,password=password,first_name=fname,last_name=lname)
		user.save()

		user = authenticate(username=uname,password=password)

		if user is not None:
			if user.is_active:
				auth_login(request,user)
				return redirect('/shop')
		else:
			return redirect('/shop/register')
		'''
		return redirect('/shop')

def login(request):
	if(request.method == 'POST'):
		email = request.POST['email']
		password = request.POST['password']

		user = authenticate(username=email,password=password)

		if user is not None:
			if user.is_active:
				auth_login(request,user)
				return redirect('/shop')
		else:
			return redirect('/shop/register')

		return redirect('/shop')
	else:
		return render(request,'login.html')

def contact_create(request):
	if(request.method == 'POST'):
		form = ContactForm(request.POST or None)
		#print form.errors
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
		else:
			print "Error !!"
		return redirect('/shop')
	else:
		form = ContactForm()
		context = {
			'form':form,
		}
		return render(request , 'contact_create.html' ,context)

def addProduct(request,id):
	if(request.method == 'POST'):
		name = request.POST['name']
		price = request.POST['price']
		description = request.POST['description']
		imgUrl = request.POST['imgUrl']

		store = Store.objects.get(id=id)

		product = Product(name=name,price=price,storeName=store.name,description=description,imgUrl=imgUrl)
		product.save()

		return redirect('/shop/details/'+id)
	else:
		store = Store.objects.get(id=id)
		context = {
			'store':store,
		}
		print store.name
		return render(request,'addProduct.html',context)

def details(request,id):
	store = Store.objects.get(id=id)
	products = store.product_set.all()
	print products
	'''
	for product in products:
		if product.store:
			print product.store.name + " --  " + store.name
			print product.store.name == store.name
	'''
	context = {
		'store':store,
		'products':products,
	}
	return render(request,'details.html',context)

def deleteStore(request,id):
	Store.objects.filter(id=id).delete()
	return redirect('/shop')

def deleteProduct(request,id):
	product = Product.objects.get(id=id)
	store = product.store
	Product.objects.filter(id=id).delete()
	return redirect('/shop/details/'+str(store.id))

def newStore(request):
	if(request.method == 'POST'):
		name = request.POST['name']
		description = request.POST['description']
		imgUrl = request.POST['imgUrl']

		store = Store(name=name,description=description,img=imgUrl)
		store.save()

		return redirect('/shop')
	else:
		return render(request,'newStore.html')

def logout(request):
	auth_logout(request)
	return redirect('/shop')
