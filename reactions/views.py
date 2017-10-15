from django.shortcuts import render , redirect
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from shop.models import Product
from notifications.models import Notification
from django.shortcuts import get_object_or_404
from reactions.models import Reaction 
# Create your views here.

def reactionRemove(request,id):
    if not request.user.is_authenticated():
        raise Http404
        
    product = get_object_or_404(Product,id=id)
    reaction = get_object_or_404(Reaction,user=request.user,product=product)
    reaction.delete()

    ret = Reaction.objects.filter(product=product).count()

    print("reaction removed successfully from reactions application...")

    return HttpResponse(ret)

def reactionNormal(request,id):
    if not request.user.is_authenticated():
        raise Http404
    print("this should work !")
    product = get_object_or_404(Product,id=id)
        
    oldReaction = Reaction.objects.filter(user=request.user,product=product)
    for old in oldReaction:
        old.delete()

    reaction = Reaction(user=request.user,product=product,reaction_type='normal')
    reaction.save()

    if request.user.id != product.table.user.id:
        notif = Notification(from_user=request.user,to_user=product.table.user,
                            notification_type='normal',product=product)
        notif.save()

    ret = Reaction.objects.filter(product=product).count()
    print("reaction --Normal-- added  successfully from reactions application...")

    return HttpResponse(ret)

def reactionSmile(request,id):
    if not request.user.is_authenticated():
        raise Http404
    print("this should work !")
    product = get_object_or_404(Product,id=id)

    oldReaction = Reaction.objects.filter(user=request.user,product=product)
    for old in oldReaction:
        old.delete()

    reaction = Reaction(user=request.user,product=product,reaction_type='smile')
    reaction.save()

    if request.user.id != product.table.user.id:
        notif = Notification(from_user=request.user,to_user=product.table.user,
                            notification_type='smile',product=product)
        notif.save()

    ret = Reaction.objects.filter(product=product).count()
    print("reaction --Smile-- added  successfully from reactions application...")

    return HttpResponse(ret)

def reactionLove(request,id):
    if not request.user.is_authenticated():
        raise Http404
    print("this should work !")
    product = get_object_or_404(Product,id=id)

    oldReaction = Reaction.objects.filter(user=request.user,product=product)
    for old in oldReaction:
        old.delete()

    reaction = Reaction(user=request.user,product=product,reaction_type='love')
    reaction.save()

    if request.user.id != product.table.user.id:
        notif = Notification(from_user=request.user,to_user=product.table.user,
                            notification_type='love',product=product)
        notif.save()

    ret = Reaction.objects.filter(product=product).count()
    print("reaction --Love-- added  successfully from reactions application...")

    return HttpResponse(ret)

def reactionWish(request,id):
    if not request.user.is_authenticated():
        raise Http404
    print("this should work !")
    product = get_object_or_404(Product,id=id)
    
    oldReaction = Reaction.objects.filter(user=request.user,product=product)
    for old in oldReaction:
        old.delete()
        
    reaction = Reaction(user=request.user,product=product,reaction_type='wish')
    reaction.save()

    if request.user.id != product.table.user.id:
        notif = Notification(from_user=request.user,to_user=product.table.user,
                            notification_type='wish',product=product)
        notif.save()

    ret = Reaction.objects.filter(product=product).count()
    print("reaction --Wish-- added  successfully from reactions application...")

    return HttpResponse(ret)