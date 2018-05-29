from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from .form import LoginForm
from uuid import uuid4
from .models import User, UuidUser
from datetime import datetime


# Create your views here.


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            email = user_data.get('email')
            uuid = str(uuid4())
            try:
                user = User.objects.get(email=email)
                name = user.name
                User.objects.filter(email=email).update(last_login_date=datetime.now())
                UuidUser.objects.filter(user_uuid__email=email).update(uuid=uuid)

            except User.DoesNotExist:
                if user_data.get('last_name'):
                    name = user_data.get('last_name')
                else:
                    name = email.split('@')[0]
                user = User.objects.create(
                    name=name,
                    email=email,
                    reg_date=datetime.now(),
                    last_login_date=datetime.now(),
                )
                UuidUser.objects.create(user_uuid=user, uuid=uuid)

            return render(request, 'url.html', {
                        'name': name,
                        'uuid': uuid,
                        'path': request.get_host(),
                    })
        else:
            redirect('/login/')
    else:
        form = LoginForm()
    return render(request, 'login.html', {
            'form': form,
    })

def url(request):

    return redirect('/login/')

def enter(request, uuid):
    user = User.objects.get(uuiduser__uuid=uuid)

    return render(request, 'login.html', {
                        'name': user.name,})

