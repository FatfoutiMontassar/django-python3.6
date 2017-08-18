from django.shortcuts import render , redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from authentication.forms import ProfileForm
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
                        return redirect('/discover')
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
                return redirect('/discover')
        else:
            return redirect('/authentication/login')

        return redirect('/discover')
    else:
        return render(request, 'login.html')

def settings(request):
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.profile.job_title = form.cleaned_data.get('job_title')
            user.email = form.cleaned_data.get('email')
            user.profile.url = form.cleaned_data.get('url')
            user.profile.location = form.cleaned_data.get('location')
            user.save()
            messages.add_message(request,
                                 messages.SUCCESS,
                                 'Your profile was successfully edited.')

    else:
        form = ProfileForm(instance=user, initial={
            'job_title': user.profile.job_title,
            'url': user.profile.url,
            'location': user.profile.location
            })
    return render(request, 'authentication/settings.html', {'form': form})

def picture(request):
    uploaded_picture = False
    try:
        if request.GET.get('upload_picture') == 'uploaded':
            uploaded_picture = True

    except Exception:
        pass

    return render(request, 'authentication/picture.html',
                  {'uploaded_picture': uploaded_picture})


def upload_picture(request):
    try:
        profile_pictures = django_settings.MEDIA_ROOT + '/profile_picture/'
        if not os.path.exists(profile_pictures):
            os.makedirs(profile_pictures)
        f = request.FILES['picture']
        filename = profile_pictures + request.user.username + '_tmp.jpg'
        with open(filename, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)
        im = Image.open(filename)
        width, height = im.size
        if width > 350:
            new_width = 350
            new_height = (height * 350) / width
            new_size = new_width, new_height
            im.thumbnail(new_size, Image.ANTIALIAS)
            im.save(filename)

        return redirect('/settings/picture/?upload_picture=uploaded')

    except Exception as e:
        print(e)
        return redirect('/settings/picture/')


def password(request):
    user = request.user
    return render(request, 'authentication/password.html')

def logout(request):
    auth_logout(request)
    return redirect('/discover')
