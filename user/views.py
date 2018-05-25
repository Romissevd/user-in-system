from django.shortcuts import render, redirect
from .form import LoginForm
from uuid import uuid4
from .models import User
from datetime import datetime


# Create your views here.


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_data = form.cleaned_data
            email = user_data.get('email')
            try:
                user = User.objects.get(email=email)
                name = user.name
            except User.DoesNotExist:
                if user_data.get('last_name'):
                    name = user_data.get('last_name')
                else:
                    name = email.split('@')[0]
                User.objects.create(
                    name=name,
                    email=email,
                    reg_date=datetime.now(),
                    last_login_date=datetime.now(),
                )

            return render(request, 'login.html', {
                        'name': name,
                        'uuid': str(uuid4()),
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
    #User.objects.filter(name=)

    return redirect('/login/')

