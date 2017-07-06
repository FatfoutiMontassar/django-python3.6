# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth import authenticate

from django.contrib.auth import login as auth_login, logout as auth_logout

from django.shortcuts import render, redirect

from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User

from django.http import HttpResponse, Http404

from .models import Product, Store, Contact, StoreImage, ProductMainImage, ProductSecImage

from .forms import StoreForm, ProductForm, ContactForm, EditProductForm, StoreImageForm, addProductMainImageForm, \
    productSImageForm

from django.shortcuts import get_object_or_404

from django.core.paginator import Paginator

import re

# Create your views here.

categoriesList = ["Vétement et accessoires", "Bijoux", "Founiture créatives", "Mariages", "Maison", "Enfant et bébé"]


def getCount(categorie):
    products = Product.objects.all()
    return products.filter(categorie=categorie).count()


def getCountFromList(categorie, tab):
    ret = 0
    for x in tab:
        if x.categorie == categorie:
            ret += 1
    return ret


def getId(cat):
    id = 1
    for x in categoriesList:
        if cat == x:
            return id
        id += 1
    return 0


def getMainImage(product):
    imgs = ProductMainImage.objects.filter(product=product).order_by("-created_at")
    img = None
    if imgs:
        img = imgs[0]
    return img


def getStoreImage(store):
    imgs = StoreImage.objects.filter(store=store).order_by("-created_at")
    img = None
    if imgs:
        img = imgs[0]
    return img


def match(str1, str2):
    str1 = str1.lower()
    str2 = str2.lower()
    # print str1 + " -- " + str2
    for i in range(0, len(str2) - len(str1) + 1):
        # print " i :: " + str(i) + str2[i]
        flag = True
        for j in range(0, len(str1)):
            # print "    j :: " + str(j) + str1[j]
            if str1[j] != str2[i + j]:
                flag = False
                break
        if flag:
            return True
    return False


def album(request, id):
    if (request.method == 'POST'):
        form = productSImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.product = Product.objects.get(id=id)
            instance.save()
            return redirect('/shop/album/' + str(id))
        else:
            print "error !!"
            print form.errors
            # print form.errors
            return redirect('/shop/album/' + str(id))
        return redirect(request, '/shop/album/' + str(id))
    else:
        product = get_object_or_404(Product, id=id)
        form = productSImageForm()
        imgs = ProductSecImage.objects.filter(product=product).order_by("-created_at")
        context = {
            'product': product,
            'form': form,
            'imgs': imgs,
        }
        return render(request, 'album.html', context)


def editStore(request, id):
    if not request.user.is_authenticated():
        raise Http404

    if (not request.user.id == get_object_or_404(Store, id=id).user.id):
        raise Http404

    if (request.method == 'POST'):
        form = StoreForm(request.POST or None)

        if form.is_valid():
            store = get_object_or_404(Store, id=id)
            store.name = form.cleaned_data['name']
            store.description = form.cleaned_data['description']
            store.phoneNumber = form.cleaned_data['phoneNumber']
            store.facebookPage = form.cleaned_data['facebookPage']
            store.locationUrl = form.cleaned_data['locationUrl']
            store.isActive = form.cleaned_data['isActive']

            # print product.name
            # print str(product.id)
            store.save()
        else:
            print "Error !!"
        print str(id)
        return redirect('/shop/stores/' + str(id))

    else:
        store = get_object_or_404(Store, id=id)
        form = StoreForm(instance=store)
        context = {'store': store, 'form': form, }
        return render(request, 'editStore.html', context)


def duplicateProduct(request, id):
    product = get_object_or_404(Product, id=id)
    imgs = ProductMainImage.objects.filter(product=product).order_by("-created_at")
    product.id = None
    product.created_at = datetime.now()
    product.save()
    # print product.id
    if imgs:
        img = imgs[0]
        newimg = ProductMainImage(img=img.img, product=product)
        newimg.save()

    return redirect('/shop/details/' + str(product.store.id))


def activateProduct(request, id):
    product = get_object_or_404(Product, id=id)
    if product.isActive == True:
        print "become not active"
        product.isActive = False
    else:
        print "become active"
        product.isActive = True
    product.save()
    return redirect('/shop/product_details/' + str(int(id)))


def addProductMainImage(request, id):
    form = addProductMainImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.product = Product.objects.get(id=id)
        instance.save()
        return redirect('/shop/product_details/' + str(id))
    else:
        print "error !!"
        print form.errors
        # print form.errors
        return redirect('/shop/product_details/' + str(id))


def searchmore(request, cId, input):
    # print "ok"
    # return redirect('/shop')
    mapInt2String = ["Tous les categories", "Vétement et accessoires", "Bijoux", "Founiture créatives", "Mariages",
                     "Maison", "Enfant et bébé", "Boutiques", "utilisateurs"]

    categorie = ""

    for element in mapInt2String:
        if getId(element) == int(cId):
            categorie = element
            break

    wordList = re.sub("[^\w]", " ", str(input)).split()

    products = Product.objects.all().order_by("-created_at")

    '''
	if (not categorie == "Tous les categories"):
		products = products.filter(categorie=categorie)
	'''
    result = []
    tab = []
    '''
	print match("test","test")

	for word in wordList:
		print "*"+word+"*"
	'''
    for product in products:
        score = 0
        for word in wordList:
            # print word + " -- " + str(product.name)
            # print word + " -- " + str(product.description)
            if (match(word, str(product.name))):
                # print "ok"
                score += 4
            if match(word, str(product.description)):
                score += 1
        if score > 0:
            if product.categorie == categorie:
                result.append((product, score, getMainImage(product)))
            tab.append(product)
        # print product.name

    result.sort(key=lambda tup: tup[1])
    # print len(result)
    n = len(result)
    '''
	for x , scr , imgUrl in result:
		print str(scr) + " -- " + x.name + " -- " + str(imgUrl.img)
	print srchFld + " -- " + srchTxt
	'''
    context = {
        'result': reversed(result),
        'n': n,
        'input': str(input),
        'nC1': str(getCountFromList("Vétement et accessoires", tab)),
        'nC2': str(getCountFromList("Bijoux", tab)),
        'nC3': str(getCountFromList("Founiture créatives", tab)),
        'nC4': str(getCountFromList("Mariages", tab)),
        'nC5': str(getCountFromList("Maison", tab)),
        'nC6': str(getCountFromList("Enfant et bébé", tab)),
    }
    return render(request, 'search.html', context)


def search(request):
    # print "ok"
    # return redirect('/shop')
    mapInt2String = ["Tous les categories", "Vétement et accessoires", "Bijoux", "Founiture créatives", "Mariages",
                     "Maison", "Enfant et bébé", "Boutiques", "utilisateurs"]
    mapString2Int = []

    '''
		i'm gonna redirect users to /shop/search/categorieIdx/TypeIdx
		and i'm gonna pass the search items in the context
		we could actually get the results from here and send them to the next page!
	'''
    srchFld = request.POST.get('srchFld')
    categorie = request.POST.get('srchTxt')
    wordList = re.sub("[^\w]", " ", srchFld).split()

    products = Product.objects.all().order_by("-created_at")

    '''
	if (not categorie == "Tous les categories"):
		products = products.filter(categorie=categorie)
	'''

    result = []
    tab = []

    '''
	print match("test","test")

	for word in wordList:
		print "*"+word+"*"
	'''
    for product in products:
        score = 0
        for word in wordList:
            # print word + " -- " + str(product.name)
            # print word + " -- " + str(product.description)
            if (match(word, str(product.name))):
                # print "ok"
                score += 4
            if (match(word, str(product.description))):
                score += 1
        if score > 0:
            if ((product.categorie == categorie) or (categorie == "Tous les categories")):
                result.append((product, score, getMainImage(product)))
            tab.append(product)

    result.sort(key=lambda tup: tup[1])
    # print len(result)
    n = len(result)
    '''
	for x , scr , imgUrl in result:
		print str(scr) + " -- " + x.name + " -- " + str(imgUrl.img)
	print srchFld + " -- " + srchTxt
	'''
    context = {
        'result': reversed(result),
        'n': n,
        'input': str(srchFld),
        'nC1': str(getCountFromList("Vétement et accessoires", tab)),
        'nC2': str(getCountFromList("Bijoux", tab)),
        'nC3': str(getCountFromList("Founiture créatives", tab)),
        'nC4': str(getCountFromList("Mariages", tab)),
        'nC5': str(getCountFromList("Maison", tab)),
        'nC6': str(getCountFromList("Enfant et bébé", tab)),
    }
    return render(request, 'search.html', context)


def categories(request, idC, idP):
    if (int(idC) > 6 or int(idC) < 1):
        return redirect('/shop')

    products = Product.objects.all()

    products = Product.objects.all().filter(categorie=categoriesList[int(idC) - 1]).order_by("-created_at")[:180]
    # print categories[int(idC)-1]
    pages = Paginator(products, 9)
    intList = list(range(1, ((products.count() + 8) / 9) + 1))
    idList = []
    for id in intList:
        idList.append(str(id))

    verifiedId = idP
    if (int(idP) > ((products.count() + 8) / 9) or int(idP) < 1):
        verifiedId = 1
    page = pages.page(verifiedId)
    values = []

    for product in page:
        x = None
        imgs = ProductMainImage.objects.filter(product=product).order_by("-created_at")
        if imgs:
            x = imgs[0]
        values.append((product, x))

    context = {
        'page': page,
        'pageId': verifiedId,
        'idList': idList,
        'idC': idC,
        'nP': products.count(),
        'values': values,
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    # print products.count()
    return render(request, 'categories.html', context)


def discovermore(request, id):
    # print "hello from page!"
    products = Product.objects.all().order_by("-created_at")[:180]
    pages = Paginator(products, 9)
    # print "number of pages : " + str((products.count()+8)/9)
    intList = list(range(1, ((products.count() + 8) / 9) + 1))
    verifiedId = id
    values = []

    if (int(id) > ((products.count() + 8) / 9) or int(id) < 1):
        verifiedId = 1
    page = pages.page(verifiedId)

    for product in page:
        x = None
        imgs = ProductMainImage.objects.filter(product=product).order_by("-created_at")
        if imgs:
            x = imgs[0]
        values.append((product, x))

    idList = []
    for i in intList:
        idList.append(str(i))

    context = {
        'nPages': pages.num_pages,
        'values': values,
        'pageId': verifiedId,
        'page': page,
        'idList': idList,
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    # return render(request,'discover',context)
    return render(request, 'discover.html', context)


def discover(request):
    # print "hello from discover!"
    global categoriesList
    # print len(categoriesList)
    products = Product.objects.all().order_by("-created_at")[:180]
    pages = Paginator(products, 9)
    idList = list(range(1, ((products.count() + 8) / 9) + 1))
    page = pages.page(1)
    values = []
    for product in page:
        x = None
        imgs = ProductMainImage.objects.filter(product=product).order_by("-created_at")
        if imgs:
            x = imgs[0]
        values.append((product, x))

    context = {
        'nPages': pages.num_pages,
        'values': values,
        'page': page,
        'pageId': 1,
        'idList': idList,
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    return render(request, 'discover.html', context)


def product_details(request, id):
    product = Product.objects.get(id=id)
    form = addProductMainImageForm()
    editProductForm = ProductForm(instance=product)

    img = getMainImage(product)

    context = {
        'form': form,
        'product': product,
        'img': img,
        'editProductForm': editProductForm,
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),

    }
    return render(request, 'product_details.html', context)


def store_details(request, id):
    store = Store.objects.get(id=id)
    form = StoreImageForm()
    context = {
        'store': store,
        'form': form,
        'nC1': getCount(categories[0]),
        'nC2': getCount(categories[1]),
        'nC3': getCount(categories[2]),
        'nC4': getCount(categories[3]),
        'nC5': getCount(categories[4]),
        'nC6': getCount(categories[5]),
    }
    return render(request, 'store_details.html', context)


def editProduct(request, id):
    if not request.user.is_authenticated():
        raise Http404

    if (not request.user.id == get_object_or_404(Product, id=id).store.user.id):
        raise Http404

    if (request.method == 'POST'):

        form = ProductForm(request.POST or None)

        if form.is_valid():
            product = get_object_or_404(Product, id=id)
            product.name = form.cleaned_data['name']
            product.price = form.cleaned_data['price']
            product.categorie = form.cleaned_data['categorie']
            product.description = form.cleaned_data['description']
            product.quantity = form.cleaned_data['quantity']
            product.quantity = form.cleaned_data['quantity']
            product.Ptype = form.cleaned_data['Ptype']

            # print product.name
            # print str(product.id)
            product.save()
        else:
            print "Error !!"
        return redirect('/shop/product_details/' + str(id))
    else:
        product = get_object_or_404(Product, id=id)
        form = ProductForm(instance=product)
        context = {
            'product': product,
            'form': form,
        }
        return render(request, 'editProduct.html', context)


def product_create(request, id):
    if not request.user.is_authenticated():
        raise Http404

    if (not request.user.id == Store.objects.get(id=id).user.id):
        raise Http404
    else:
        if (request.method == 'POST'):
            form = ProductForm(request.POST or None, request.FILES or None)
            print form.errors
            print form
            if form.is_valid():
                instance = form.save(commit=False)
                store = Store.objects.get(id=id)
                # print instance
                instance.store = store
                instance.isActive = False
                instance.save()
            else:
                print "Error !!"
            return redirect('/shop/details/' + id)
        else:
            store = Store.objects.get(id=id)
            form = ProductForm()
            context = {
                'form': form,
                'store': store,
            }
            # print store.name
            return render(request, 'product_form.html', context)


def store_create(request):
    if not request.user.is_authenticated():
        raise Http404
    else:
        if (request.method == 'POST'):
            form = StoreForm(request.POST or None, request.FILES or None)
            # print form.errors
            if form.is_valid():
                instance = form.save(commit=False)
                if (Store.objects.filter(name=instance.name).filter(user=request.user).exists()):
                    form = StoreForm()
                    context = {
                        'form': form,
                        'error_message': "Error !! you have already created a store with the same name",
                    }
                    return render(request, 'store_form.html', context)
                else:
                    instance.user = request.user
                    instance.save()
                    return redirect('/shop/stores')
            else:
                form = StoreForm()

                context = {
                    'form': form,
                    'error_message': "Error !! form is not valid",
                }
                return render(request, 'store_form.html', context)
        else:
            additional = ""
            if not hasattr(request.user,'trader'):
                additional = "this is your first store !!"
            
            form = StoreForm()
            context = {
                'form': form,
                'additional':additional,
            }
            return render(request, 'store_form.html', context)


def storesView(request):
    stores = Store.objects.all()[:18]
    values = []
    for store in stores:
        values.append((store, getStoreImage(store)))
    for a, b in values:
        print a, b
    context = {
        'values': values,
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    return render(request, 'stores.html', context)


def product(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)


# the trick is to use email as username and username as email :p (it will work perfecty as us username is unique)
def register(request):
    if (request.method == 'POST'):
        # uname = request.POST['uname']
        email = request.POST['email']
        # fname = request.POST['fname']
        # lname = request.POST['lname']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if (password == confirmPassword):
            print "password == confirmPassword"
            if (User.objects.filter(username=email).exists()):
                print("Error , acout alreasy exists")
            else:
                user = User.objects.create_user(username=email, password=password)
                user.save()
                user = authenticate(username=email, password=password)
                if user is not None:
                    if user.is_active:
                        auth_login(request, user)
                        return redirect('/shop')
                else:
                    return redirect('/shop/login')
        else:
            print "password and confirmation password dont match !"
        return redirect('/shop')


def login(request):
    if (request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/shop')
        else:
            return redirect('/shop/register')

        return redirect('/shop')
    else:
        return render(request, 'login.html')


def contact_create(request):
    if (request.method == 'POST'):
        form = ContactForm(request.POST or None)
        # print form.errors
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
        else:
            print "Error !!"
        return redirect('/shop')
    else:
        form = ContactForm()
        context = {
            'form': form,
        }
        return render(request, 'contact_create.html', context)


def addProduct(request, id):
    if (request.method == 'POST'):
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        imgUrl = request.POST['imgUrl']

        store = Store.objects.get(id=id)

        product = Product(name=name, price=price, storeName=store.name, description=description, imgUrl=imgUrl)
        product.save()

        return redirect('/shop/details/' + id)
    else:
        store = Store.objects.get(id=id)
        context = {
            'store': store,
        }
        print store.name
        return render(request, 'addProduct.html', context)


def details(request, id):
    # print str(id)
    store = Store.objects.get(id=id)
    products = store.product_set.all().order_by("-created_at")
    nP = products.count()
    form = StoreImageForm()
    imgs = StoreImage.objects.filter(store=store).order_by("-created_at")
    pages = Paginator(products, 9)
    page = pages.page(1)
    values = []
    for product in page:
        x = None
        Pimgs = ProductMainImage.objects.filter(product=product).order_by("-created_at")

        if Pimgs:
            x = Pimgs[0]
        values.append((product, x))

    intList = list(range(1, ((products.count() + 8) / 9) + 1))
    idList = []
    for i in intList:
        idList.append(str(i))

    if imgs:
        img = imgs[0]
        # print img.img

        context = {
            'store': store,
            'values': values,
            'form': form,
            'img': img,
            'page': page,
            'nP': nP,
            'idList': idList,
            'pageId': "1",
            'idS': str(id),
            'nC1': getCount(categoriesList[0]),
            'nC2': getCount(categoriesList[1]),
            'nC3': getCount(categoriesList[2]),
            'nC4': getCount(categoriesList[3]),
            'nC5': getCount(categoriesList[4]),
            'nC6': getCount(categoriesList[5]),
        }
    else:
        context = {
            'store': store,
            'values': values,
            'form': form,
            'page': page,
            'nP': nP,
            'idList': idList,
            'pageId': "1",
            'idS': str(id),
            'nC1': getCount(categoriesList[0]),
            'nC2': getCount(categoriesList[1]),
            'nC3': getCount(categoriesList[2]),
            'nC4': getCount(categoriesList[3]),
            'nC5': getCount(categoriesList[4]),
            'nC6': getCount(categoriesList[5]),
        }
    print str(id)
    return render(request, 'details.html', context)


def detailsMore(request, idS, idP):
    store = Store.objects.get(id=idS)
    products = store.product_set.all().order_by("-created_at")
    nP = products.count()
    form = StoreImageForm()
    imgs = StoreImage.objects.filter(store=store).order_by("-created_at")
    pages = Paginator(products, 9)
    page = pages.page(int(idP))
    values = []
    for product in page:
        x = None
        Pimgs = ProductMainImage.objects.filter(product=product).order_by("-created_at")

        if Pimgs:
            x = Pimgs[0]
        values.append((product, x))

    intList = list(range(1, ((products.count() + 8) / 9) + 1))
    idList = []
    for i in intList:
        idList.append(str(i))

    if imgs:
        img = imgs[0]
        # print img.img

        context = {
            'store': store,
            'values': values,
            'form': form,
            'img': img,
            'page': page,
            'nP': nP,
            'idList': idList,
            'pageId': str(idP),
            'idS': str(idS),
            'nC1': getCount(categoriesList[0]),
            'nC2': getCount(categoriesList[1]),
            'nC3': getCount(categoriesList[2]),
            'nC4': getCount(categoriesList[3]),
            'nC5': getCount(categoriesList[4]),
            'nC6': getCount(categoriesList[5]),
        }
    else:
        context = {
            'store': store,
            'values': values,
            'form': form,
            'page': page,
            'nP': nP,
            'idList': idList,
            'pageId': str(idP),
            'idS': str(idS),
            'nC1': getCount(categoriesList[0]),
            'nC2': getCount(categoriesList[1]),
            'nC3': getCount(categoriesList[2]),
            'nC4': getCount(categoriesList[3]),
            'nC5': getCount(categoriesList[4]),
            'nC6': getCount(categoriesList[5]),
        }
    print str(idS)
    return render(request, 'details.html', context)


def addStoreImage(request, id):
    form = StoreImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.store = Store.objects.get(id=id)
        instance.save()
        return redirect('/shop/stores')
    else:
        print "error !!"
        print form.errors
        # print form.errors
        return redirect('/shop/stores')


def deleteStore(request, id):
    Store.objects.filter(id=id).delete()
    return redirect('/shop')


def deleteProduct(request, id):
    print "delete : " + str(id)
    product = Product.objects.get(id=id)
    store = product.store
    Product.objects.filter(id=id).delete()
    return redirect('/shop/details/' + str(store.id))


def newStore(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        description = request.POST['description']
        imgUrl = request.POST['imgUrl']

        store = Store(name=name, description=description, img=imgUrl)
        store.save()

        return redirect('/shop')
    else:
        return render(request, 'newStore.html')


def logout(request):
    auth_logout(request)
    return redirect('/shop')
