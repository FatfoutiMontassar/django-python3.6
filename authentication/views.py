from django.shortcuts import render , redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
# Create your views here.
def register(request):
    if (request.method == 'POST'):
        print("register function called from authentication ...")
        # uname = request.POST['uname']
        email = request.POST['email']
        # fname = request.POST['fname']
        # lname = request.POST['lname']
        password = request.POST['password']
        confirmPassword = request.POST['confirmPassword']

        if (password == confirmPassword):
            #print "password == confirmPassword"
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
                    return redirect('/authentication/login')
        else:
            print "password and confirmation password dont match !"
        return redirect('/authentication/login')


def login(request):
    if (request.method == 'POST'):
        print "login function from authentication called .."
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return redirect('/shop')
        else:
            return redirect('/authentication/login')

        return redirect('/shop')
    else:
        return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('/shop')
