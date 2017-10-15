# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from .models import Product, Table, Contact, TableImage, ProductMainImage, ProductSecImage , Trader , albumImage
from .forms import TableForm, ProductForm, ContactForm, EditProductForm, TableImageForm, addProductMainImageForm, \
    productSImageForm , TraderForm , albumImageForm
from authentication.models import Profile
#from discover.views import getRecs  
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
import re
from django.views.generic import RedirectView
from messenger.models import Message
import json
import math
from authentication.models import Activity
# Create your views here.


categoriesList = ["Vetement et accessoires", "Bijoux", "Founiture creatives", "Mariages", "Maison", "Enfant et bebe"]

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

    for table in Table.objects.all():
        if len(ret) >= 2:
                break
        if table.get_image():
            ret.append( table.get_image() )
            
    return ret

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
    return product.get_image



def getTableImage(table):
    imgs = TableImage.objects.filter(table=table).order_by("-created_at")
    img = None
    if imgs:
        img = imgs[0]
    return img

def getSecImages(product):
    imgs = ProductSecImage.objects.filter(product=product).order_by("-created_at")
    ret = []

    #print "images here :: " + str(imgs.count())
    for img in imgs:
        ret.append(img)
        #print " --  : " + str(img.img)
    return ret

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

def products(request):

    ans = Product.objects.all()
    ret = []
    template = '{0} ({1})'
    for p in ans:
        ret.append(p.name)
    data = json.dumps(ret)
    return HttpResponse(data,content_type='application/json')

def album(request, id):
    if (request.method == 'POST'):
        form = productSImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.product = Product.objects.get(id=id)
            instance.save()
            return redirect('/shop/album/' + str(id))
        else:
            #print "error !!"
            # print form.errors
            return redirect('/shop/album/' + str(id))
        return redirect(request, '/shop/album/' + str(id))
    else:
        product = get_object_or_404(Product, id=id)
        form = productSImageForm()
        imgs = ProductSecImage.objects.filter(product=product).order_by("-created_at")
        rec = getRecs()
        rec1 = rec[0]
        rec2 = rec[1]
        context = {
            'rec1':rec1,
            'rec2':rec2,
            'product': product,
            'form': form,
            'imgs': imgs,
        }
        return render(request, 'album.html', context)


def editTable(request, id):
    if not request.user.is_authenticated():
        raise Http404

    if (not request.user.id == get_object_or_404(Table, id=id).user.id):
        raise Http404

    if (request.method == 'POST'):
        form = TableForm(request.POST or None)

        if form.is_valid():
            table = get_object_or_404(Table, id=id)
            table.name = form.cleaned_data['name']
            table.description = form.cleaned_data['description']
            table.phoneNumber = form.cleaned_data['phoneNumber']
            table.facebookPage = form.cleaned_data['facebookPage']
            table.locationUrl = form.cleaned_data['locationUrl']
            table.isActive = form.cleaned_data['isActive']

            # print product.name
            # print str(product.id)
            table.save()
            return redirect('/shop/tables/' + str(id))

    else:
        table = get_object_or_404(Table, id=id)
        form = TableForm(instance=table)
        rec = getRecs()
        rec1 = rec[0]
        rec2 = rec[1]
        context = {
            'rec1':rec1,
            'rec2':rec2,
            'table': table, 
            'form': form, 
        }
        return render(request, 'editTable.html', context)


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

    return redirect('/shop/details/' + str(product.table.id))


def activateProduct(request, id):
    product = get_object_or_404(Product, id=id)
    if product.isActive == True:
        #print "become not active"
        product.isActive = False
    else:
        #print "become active"
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
        #print "error !!"
        #print form.errors
        # print form.errors
        return redirect('/shop/product_details/' + str(id))


def product_details(request, id):
    #recs = getRecs()
    #print("the length of the returned list from getRecs function : ",len(recs))
    product = Product.objects.get(id=id)

    if request.user.is_authenticated():
        activity = Activity(user=request.user,product=product)
        activity.save()

    form = addProductMainImageForm()
    editProductForm = ProductForm(instance=product)

    img = getMainImage(product)

    imgs = getSecImages(product)

    #print imgs
    rec = getRecs()
    rec1 = rec[0]
    rec2 = rec[1]
    context = {
        'rec1':rec1,
        'rec2':rec2,
        'form': form,
        'product': product,
        'img': img,
        'imgs':imgs,
        'editProductForm': editProductForm,
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),

    }
    return render(request, 'product_details.html', context)


def table_details(request, id):
    table = Table.objects.get(id=id)

    if request.user.is_authenticated():
        activity = Activity(user=request.user,table=table)
        activity.save()

    form = TableImageForm()
    rec = getRecs()
    rec1 = rec[0]
    rec2 = rec[1]
    context = {
        'rec1':rec1,
        'rec2':rec2,
        'table': table,
        'form': form,
        'nC1': getCount(categories[0]),
        'nC2': getCount(categories[1]),
        'nC3': getCount(categories[2]),
        'nC4': getCount(categories[3]),
        'nC5': getCount(categories[4]),
        'nC6': getCount(categories[5]),
    }
    return render(request, 'table_details.html', context)


def editProduct(request, id):
    if not request.user.is_authenticated():
        raise Http404

    if (not request.user.id == get_object_or_404(Product, id=id).table.user.id):
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
        return redirect('/shop/product_details/' + str(id))
    else:
        product = get_object_or_404(Product, id=id)
        form = ProductForm(instance=product)
        rec = getRecs()
        rec1 = rec[0]
        rec2 = rec[1]
        context = {
            'rec1':rec1,
            'rec2':rec2,
            'product': product,
            'form': form,
        }
        return render(request, 'editProduct.html', context)


def product_create(request, id):
    if not request.user.is_authenticated():
        raise Http404

    if (not request.user.id == Table.objects.get(id=id).user.id):
        raise Http404
    else:
        if (request.method == 'POST'):
            form = ProductForm(request.POST or None, request.FILES or None)
            #print form.errors
            #print form
            if form.is_valid():
                instance = form.save(commit=False)
                table = Table.objects.get(id=id)
                # print instance
                instance.table = table
                instance.isActive = False
                instance.save()
            return redirect('/shop/details/' + id)
        else:
            table = Table.objects.get(id=id)
            form = ProductForm()
            rec = getRecs()
            rec1 = rec[0]
            rec2 = rec[1]
            context = {
                'rec1':rec1,
                'rec2':rec2,
                'form': form,
                'table': table,
            }
            # print table.name
            return render(request, 'product_form.html', context)

def table_create(request,comment):
    if not request.user.is_authenticated():
        raise Http404
    else:
        if (request.method == 'POST'):
            if(str(comment) == "ok"):
                form = TableForm(request.POST or None, request.FILES or None)
                # print form.errors
                if form.is_valid():
                    instance = form.save(commit=False)
                    if (Table.objects.filter(name=instance.name).filter(user=request.user).exists()):
                        form = TableForm()
                        context = {
                            'form': form,
                            'error_message': "Error !! you have already created a table with the same name",
                        }
                        return render(request, 'table_form.html', context)
                    else:
                        instance.user = request.user
                        instance.save()
                        return redirect('/shop/tables')
                else:
                    form = TableForm()

                    context = {
                        'form': form,
                        'error_message': "Error !! form is not valid",
                    }
                    return render(request, 'table_form.html', context)
            elif(str(comment) == "addStatus"):
                form = TraderForm(request.POST or None)
                if form.is_valid:
                    instance = form.save(commit=False)
                    instance.user = request.user
                    instance.save()
                    return redirect('/shop/table_create/verifyFirst')
                else:
                    return redirect('/shop/tables/')
            else:
                raise Http404

        else:
            rec = getRecs()
            rec1 = rec[0]
            rec2 = rec[1]
            if not hasattr(request.user,'trader'):
                additional = "this is your first table !! please select your status"
                form = TraderForm()
                context = {
                    'rec1':rec1,
                    'rec2':rec2,
                    'form': form,
                    'additional':additional,
                }
                return render(request, 'table_form.html', context)
            else:
                form = TableForm()
                context = {
                    'rec1':rec1,
                    'rec2':rec2,
                    'form': form,
                }
                return render(request, 'table_form.html', context)

def tablesView(request):
    tables = Table.objects.all()[:18]
    values = []
    for table in tables:
        values.append((table, getTableImage(table)))
    
    rec = getRecs()
    rec1 = rec[0]
    rec2 = rec[1]
    
    context = {
        'rec1':rec1,
        'rec2':rec2,
        'values': values,
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    return render(request, 'tables.html', context)


def product(request, id):
    product = Product.objects.get(id=id)
    context = {
        'product': product
    }
    return render(request, 'product.html', context)


def contact_create(request):
    if (request.method == 'POST'):
        form = ContactForm(request.POST or None)
        # print form.errors
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
        else:
            print("Error !!")
        return redirect('/shop')
    else:
        form = ContactForm()
        rec = getRecs()
        rec1 = rec[0]
        rec2 = rec[1]
        context = {
            'rec1':rec1,
            'rec2':rec2,
            'form': form,
        }
        return render(request, 'contact_create.html', context)


def addProduct(request, id):
    if (request.method == 'POST'):
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        imgUrl = request.POST['imgUrl']

        table = Table.objects.get(id=id)

        product = Product(name=name, price=price, tableName=table.name, description=description, imgUrl=imgUrl)
        product.save()

        return redirect('/shop/details/' + id)
    else:
        table = Table.objects.get(id=id)
        rec = getRecs()
        rec1 = rec[0]
        rec2 = rec[1]
        context = {
            'rec1':rec1,
            'rec2':rec2,
            'table': table,
        }
        print(table.name)
        return render(request, 'addProduct.html', context)


def details(request, id,idP="1"):
    # print str(id)

    Ptype = request.GET.get('Ptype', 'all')
    #print Ptype

    Prange = request.GET.get('Prange', 'all')
    #print Prange

    table = Table.objects.get(id=id)
    products = table.product_set.all().order_by("-created_at")

    Pmin = request.GET.get('Pmin',0)
    Pmax = request.GET.get('Pmax',10000)

    products = products.filter(price__gte=Pmin)
    products = products.filter(price__lte=Pmax)

    if(Ptype=="handMade"):
        products = products.filter(Ptype=1)
    if(Ptype=="vintage"):
        products = products.filter(Ptype=2)

    if(Prange == "range1"):
        products = products.filter(price__gte=1)
        products = products.filter(price__lte=50)
    if(Prange == "range2"):
        products = products.filter(price__gte=50)
        products = products.filter(price__lte=1000)
    if(Prange == "range3"):
        products = products.filter(price__gte=1000)
        products = products.filter(price__lte=100000)

    nP = products.count()
    form = TableImageForm()
    imgs = TableImage.objects.filter(table=table).order_by("-created_at")
    pages = Paginator(products, 9)
    vId = int(idP)
    if( ( vId > int((nP+8)/9) ) or (vId < 1) ):
        vId = 1
    page = pages.page(vId)
    values = []
    for product in page:
        x = getMainImage(product)
        #print x
        values.append((product, x))

    intList = list(range(1, math.floor((products.count() + 8) / 9) + 1))
    idList = []
    for i in intList:
        idList.append(str(i))

    filters = "?Ptype="+str(Ptype)+"&Pmin="+str(Pmin)+"&Pmax="+str(Pmax)
    rec = getRecs()
    rec1 = rec[0]
    rec2 = rec[1]
    context = {
        'rec1':rec1,
        'rec2':rec2,
        'table': table,
        'values': values,
        'form': form,
        'page': page,
        'nP': nP,
        'Pmin':Pmin,
        'Pmax':Pmax,
        'idList': idList,
        'pageId': "1",
        'filters':filters,
        'Ptype':str(Ptype),
        'Prange':str(Prange),
        'idS': str(id),
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    if imgs:
        context['img'] = imgs[0]
        # print img.img

    #print str(id)
    return render(request, 'details.html', context)

def tablesAlbum(request,id):
    if(request.method == 'POST'):
        form = albumImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.table = Table.objects.get(id=id)
            instance.save()
            return redirect('/shop/tablesAlbum/' + str(id))
        else:
            #print "error !!"
            # print form.errors
            return redirect('/shop/tablesAlbum/' + str(id))
        return redirect(request, '/shop/tablesAlbum/' + str(id))
    else:
        form = albumImageForm()
        table = get_object_or_404(Table,id=id)
        imgs = albumImage.objects.filter(table=table)
        rec = getRecs()
        rec1 = rec[0]
        rec2 = rec[1]
        context = {
            'rec1':rec1,
            'rec2':rec2,
            'imgs':imgs,
            'form':form,
        }
        return render(request,'album.html',context)

def wishlist(request):
    profile = get_object_or_404(Profile,user=request.user)
    products = []
    for pr in profile.wishedProducts.all():
        products.append(pr)
    collections = []
    for cl in profile.wishedCollections.all():
        collections.append(cl)

    rec = getRecs()
    rec1 = rec[0]
    rec2 = rec[1]
    context = {
        'rec1':rec1,
        'rec2':rec2,
        'products':products,
        'collections':collections
    }
    return render(request,'wishlist.html',context)

def view(request, id,idP="1"):
    # print str(id)
    Ptype = request.GET.get('Ptype', 'all')
    #print Ptype

    Prange = request.GET.get('Prange', 'all')
    #print Prange

    table = Table.objects.get(id=id)


    if request.user.is_authenticated():
        activity = Activity(user=request.user,table=table)
        activity.save()

    # send message to table's owner
    if request.user != table.user:
        if(not (request.user in table.visitors.all())):
            print("visit ...")
            message = "This is an automatically generated message, welcome to my table ( " + str(table.name) + " ) , if you have any questions, please feel free :) "
            if table.user.profile.message != None:
                message = str(table.user.profile.message)
            msg = Message.send_message(table.user,request.user,message).save()
            table.visitors.add(request.user)


    products = table.product_set.all().order_by("-created_at")

    Pmin = request.GET.get('Pmin',0)
    Pmax = request.GET.get('Pmax',10000)

    products = products.filter(price__gte=Pmin)
    products = products.filter(price__lte=Pmax)

    if(Ptype=="handMade"):
        products = products.filter(Ptype=1)
    if(Ptype=="vintage"):
        products = products.filter(Ptype=2)

    nP = products.count()
    imgs = TableImage.objects.filter(table=table).order_by("-created_at")
    pages = Paginator(products, 9)
    vId = int(idP)
    if( ( vId > int((nP+8)/9) ) or (vId < 1) ):
        vId = 1
    page = pages.page(vId)
    values = []
    for product in page:
        x = getMainImage(product)
        #print x
        values.append((product, x,product.likes.all(),product.smiles.all(),product.wishes.all(),product.likes.count()+product.smiles.count()+product.wishes.count()))

    intList = list(range(1, math.floor((products.count() + 8) / 9) + 1))
    idList = []
    for i in intList:
        idList.append(str(i))

    filters = "?Ptype="+str(Ptype)+"&Pmin="+str(Pmin)+"&Pmax="+str(Pmax)

    rec = getRecs()
    rec1 = rec[0]
    rec2 = rec[1]
    context = {
        'rec1':rec1,
        'rec2':rec2,
        'flag':'yes',
        'table': table,
        'values': values,
        'page': page,
        'nP': nP,
        'Pmin':Pmin,
        'Pmax':Pmax,
        'idList': idList,
        'pageId': str(vId),
        'filters':filters,
        'Ptype':str(Ptype),
        'Prange':str(Prange),
        'idS': str(id),
        'nC1': getCount(categoriesList[0]),
        'nC2': getCount(categoriesList[1]),
        'nC3': getCount(categoriesList[2]),
        'nC4': getCount(categoriesList[3]),
        'nC5': getCount(categoriesList[4]),
        'nC6': getCount(categoriesList[5]),
    }
    if imgs:
        context['img'] = imgs[0]

    return render(request, 'discover.html', context)


def addTableImage(request, id):
    form = TableImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.table = Table.objects.get(id=id)
        instance.save()
        return redirect('/shop/tables')
    else:
        print("error !!")
        #print form.errors
        # print form.errors
        return redirect('/shop/tables')


def deleteTable(request, id):
    Table.objects.filter(id=id).delete()
    return redirect('/shop')


def deleteProduct(request, id):
    #print "delete : " + str(id)
    product = Product.objects.get(id=id)
    table = product.table
    Product.objects.filter(id=id).delete()
    return redirect('/shop/details/' + str(table.id))


def newTable(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        description = request.POST['description']
        imgUrl = request.POST['imgUrl']

        table = table(name=name, description=description, img=imgUrl)
        table.save()

        return redirect('/shop')
    else:
        return render(request, 'newTable.html')
