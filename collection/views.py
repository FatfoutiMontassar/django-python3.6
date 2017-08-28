from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse, Http404
from .models import Collection
from shop.models import Product , Store
from authentication.models import Activity
from discover.views import getRecs

# Create your views here.

def collection_all(request):
    if not request.user.is_authenticated():
        raise Http404

    wishedCollections = request.user.profile.wishedCollections.all()

    ret = Collection.objects.filter(isActive=True)
    rec = getRecs()
    rec1 = rec[0]
    rec2 = rec[1]
    return render(request,'collection/collections.html',
        {'collections':ret,'wishedCollections':wishedCollections,'rec1':rec1,'rec2':rec2,})

def mineCollections(request):
    if not request.user.is_authenticated():
        raise Http404

    ret = Collection.objects.filter(user=request.user)
    rec = getRecs()
    rec1 = rec[0]
    rec2 = rec[1]
    return render(request,'collection/mesCollections.html',{'collections':ret,'rec1':rec1,'rec2':rec2})

def deleteCollection(request,id):
    #print str(id)
    Collection.objects.filter(id=id).delete()
    return redirect('/collections/mine/')

def viewCollections(request,id):
    collection = get_object_or_404(Collection,id=id)
    if request.user.is_authenticated():
        activity = Activity(user=request.user,collection=collection)
        activity.save()
    rec = getRecs()
    rec1 = rec[0]
    rec2 = rec[1]
    return render(request,'collection/viewCollection.html',{'collection':collection,'rec1':rec1,'rec2':rec2,})


def editCollections(request,id):
    if not request.user.is_authenticated():
        raise Http404

    if(request.method == 'POST'):
        name = request.POST.get('collectionName')
        description = request.POST.get('collectionDesc')
        image = request.FILES.get('collectionImageInput')
        #print(type(image))
        products = request.POST.get('relatedProducts') ;
        collection = get_object_or_404(Collection,id=str(id))
        collection.name = name
        collection.description = description
        if image:
            collection.image = image
        products = str(products)
        #print products
        products = products.split('&')
        #print products
        collection.save()
        for pr in collection.products.all():
            collection.products.remove(pr)

        for i in range(len(products) -1 ):
            pr = get_object_or_404(Product,id=str(products[i]))
            collection.products.add(pr)
        collection.save()
        return redirect('/collections')
    else:
        collection = get_object_or_404(Collection,id=id)
        ret = []
        for store in request.user.store_set.all():
            for pr in store.product_set.all():
                ret.append(pr)
        collectionProducts = []
        for pr in collection.products.all():
            collectionProducts.append(pr)

        #print(len(ret))
        rec = getRecs()
        rec1 = rec[0]
        rec2 = rec[1]
        context = {
            'rec1':rec1,
            'rec2':rec2,
            'collection':collection,
            'products':ret,
            'collectionProducts':collectionProducts,
        }
        return render(request,'collection/editCollection.html',context)

def newCollection(request):
    if not request.user.is_authenticated():
        raise Http404

    if(request.method=='POST'):
        name = request.POST.get('collectionName')
        description = request.POST.get('collectionDesc')
        image = request.FILES.get('collectionImageInput')
        print(type(image))
        products = request.POST.get('relatedProducts') ;
        collection = Collection(user=request.user,name=name,description=description,image=image)
        products = str(products)
        #print products
        products = products.split('&')
        #print products
        collection.save()
        for i in range(len(products) -1 ):
            pr = get_object_or_404(Product,id=str(products[i]))
            collection.products.add(pr)
        collection.save()
        return redirect('/collections')
    else:
        ret = []
        for store in request.user.store_set.all():
            for product in store.product_set.all():
                #print product.name
                ret.append(product)
        rec = getRecs()
        rec1 = rec[0]
        rec2 = rec[1]
        return render(request,'collection/newCollection.html',context={'products':ret,'rec1':rec1,'rec2':rec2})
