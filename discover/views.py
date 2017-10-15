# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from shop.models import Product, Table, Contact, TableImage, ProductMainImage, ProductSecImage , Trader
from shop.forms import TableForm, ProductForm, ContactForm, EditProductForm, TableImageForm, addProductMainImageForm, \
    productSImageForm , TraderForm
from django.http import HttpResponse, Http404
from collection.models import Collection
from django.core.paginator import Paginator
from reactions.models import Reaction
from shop import views
import re
# Create your views here.
categoriesList = ["Vetement et accessoires", "Bijoux", "Founiture creatives", "Mariages", "Maison", "Enfant et bebe"]
from django.shortcuts import get_object_or_404
from authentication.models import Activity
import math


def getCountFromList(categorie, tab):
    ret = 0
    for x in tab:
        if x.categorie == categorie:
            ret += 1
    return ret

def getCount(categorie):
    products = Product.objects.all()
    return products.filter(categorie=categorie).count()

def getId(cat):
    id = 1
    for x in categoriesList:
        if cat == x:
            return id
        id += 1
    return 0

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

def getRecs():
    ret = []
    activitys = Activity.objects.all().order_by("-created_at")
    for activity in activitys:
        if len(ret) >= 2:
                break
        if activity.product:
            if activity.product.get_image():
                ret.append(activity.product.get_image())
        elif activity.table:
            if activity.table.get_image():
                ret.append(activity.table.get_image())
        else:
            if activity.collection.image:
                ret.append(activity.collection.image)
                print(activity.collection.image)

    for table in Table.objects.all():
        if len(ret) >= 2:
                break
        if table.get_image():
            ret.append( table.get_image() )
            
    return ret

def search(request):
    if not request.user.is_authenticated():
        return redirect('/authentication/login/')

    # print "ok"
    # return redirect('/shop')
    Ptype = request.GET.get('Ptype', 'all')
    #print Ptype

    Pmin = request.GET.get('Pmin',0)
    Pmax = request.GET.get('Pmax',10000)

    categorie = "Tous les categories"

    srchFld = request.GET.get('q', '')

    srchTxt = request.GET.get('categorie', '')

    categorie = str(srchTxt)


    mapInt2String = ["Tous les categories", "Vetement et accessoires", "Bijoux", "Founiture creatives", "Mariages",
                     "Maison", "Enfant et bebe", "Boutiques", "utilisateurs"]
    mapString2Int = []

    '''
		i'm gonna redirect users to /shop/search/categorieIdx/TypeIdx
		and i'm gonna pass the search items in the context
		we could actually get the results from here and send them to the next page!
	'''
    #srchFld = request.POST.get('srchFld')
    #categorie = request.POST.get('srchTxt')
    wordList = re.sub("[^\w]", " ", str(srchFld) ).split()

    products = Product.objects.all().order_by("-created_at")

    if(Ptype=="handMade"):
        products = products.filter(Ptype=1)
    if(Ptype=="vintage"):
        products = products.filter(Ptype=2)

    products = products.filter(price__gte=Pmin)
    products = products.filter(price__lte=Pmax)

    result = []
    tab = []

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
                result.append((product, score, product.get_image ))
            tab.append(product)

    result.sort(key=lambda tup: tup[1])
    # print len(result)
    n = len(result)

    filters = "?Ptype="+str(Ptype)+"&Pmin="+str(Pmin)+"&Pmax="+str(Pmax)
    
    rec = getRecs()
    rec1 = rec[0]
    rec2 = rec[1]
    
    context = {
        'n': n,
        'input': str(srchFld),
        'Ptype':str(Ptype),
        'Pmin':Pmin,
        'idC':str(getId(str(categorie))),
        'Pmax':Pmax,
        'filters':filters,
        'nC1': str(getCountFromList("Vetement et accessoires", tab)),
        'nC2': str(getCountFromList("Bijoux", tab)),
        'nC3': str(getCountFromList("Founiture creatives", tab)),
        'nC4': str(getCountFromList("Mariages", tab)),
        'nC5': str(getCountFromList("Maison", tab)),
        'nC6': str(getCountFromList("Enfant et bebe", tab)),
        'rec1':rec1,
        'rec2':rec2,
        'result': reversed(result),
    }
    #print context['filters']
    #print "categorie id : " + context['idC']
    return render(request, 'search.html', context)



def discover(request,idC="0",idP="1"):
    if not request.user.is_authenticated():
        return redirect('/authentication/login/')

    #recs = getRecs()
    '''
    for i in recs:
        print(type(i))
    '''
    #print "hello from discovermore!" + str(id)

    Ptype = request.GET.get('Ptype', 'all')
    #print Ptype

    Prange = request.GET.get('Prange', 'all')
    #print Prange

    Pmin = request.GET.get('Pmin',0)
    Pmax = request.GET.get('Pmax',10000)

    products = Product.objects.all().order_by("-created_at")
    if(not int(idC) == 0):
        products = products.filter(categorie=categoriesList[int(idC)-1])

    if(Ptype=="handMade"):
        #print "shuold filter elements wich are handMade"
        products = products.filter(Ptype=1)
    if(Ptype=="vintage"):
        products = products.filter(Ptype=2)

    products = products.filter(price__gte=Pmin)
    products = products.filter(price__lte=Pmax)

    pages = Paginator(products, 9)
    # print "number of pages : " + str((products.count()+8)/9)
    intList = list(range(1, math.floor((products.count() + 8) / 9) + 1))
    verifiedId = idP
    values = []

    if (int(idP) > ((products.count() + 8) / 9) or int(idP) < 1):
        verifiedId = 1
    page = pages.page(verifiedId)

    for product in page:
            x = product.get_image
            if(product.get_discount()):
                disc = product.get_discount()
                #print disc.percentage
            else:
                print("no discount ...")

            normal = False 
            smile  = False 
            love   = False 
            wish   = False 
            if(Reaction.objects.filter(user=request.user,product=product,reaction_type='normal').count() > 0):
                normal = True

            if(Reaction.objects.filter(user=request.user,product=product,reaction_type='smile').count() > 0):
                smile = True

            if(Reaction.objects.filter(user=request.user,product=product,reaction_type='love').count() > 0):
                love = True

            if(Reaction.objects.filter(user=request.user,product=product,reaction_type='wish').count() > 0):
                wish = True

            ret = Reaction.objects.filter(product=product).count()

            values.append((product, x,normal,smile,love,wish,str(ret)))

    
    filters = "?Ptype="+str(Ptype)+"&Pmin="+str(Pmin)+"&Pmax="+str(Pmax)

    idList = []
    for i in intList:
        idList.append(str(i))

    rec = getRecs()
    rec1 = rec[0]
    rec2 = rec[1]

    wishedProducts = request.user.profile.wishedProducts.all()
    context = {
        'rec1':rec1,
        'rec2':rec2,
        'nPages': pages.num_pages,
        'values': values,
        'wishedProducts':wishedProducts,
        'pageId': verifiedId,
        'idC':str(idC),
        'page': page,
        'Pmin':str(Pmin),
        'Pmax':str(Pmax),
        'Ptype':str(Ptype),
        'idList': idList,
        'filters':filters,
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    return render(request, 'discover.html', context)


def addToWishList(request):
    if not request.user.is_authenticated():
        return redirect('/authentication/login/')

    tp = request.POST.get('type')
    id = request.POST.get('id')
    obj = None

    ret = "added"

    if(tp == "P"):
        obj = get_object_or_404(Product,id=id)
        if obj in request.user.profile.wishedProducts.all():
            request.user.profile.wishedProducts.remove(obj)
            ret = "removed"
        else:
            request.user.profile.wishedProducts.add(obj)
            ret = "added"
    else:
        obj = get_object_or_404(Collection,id=id)
        if obj in request.user.profile.wishedCollections.all():
            request.user.profile.wishedCollections.remove(obj)
            ret = "removed"
        else:
            request.user.profile.wishedCollections.add(obj)
            ret = "added"

    return HttpResponse(ret)
