from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from .form import LoginForm
from uuid import uuid4
from .models import User, UuidUser
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import EmailMessage


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
                user_name = user.name
                if (user.last_login_date + timedelta(minutes=5)) > timezone.now():
                    message_for_site = 'На Ваш email уже было отправлено сообщение.' \
                                       'Проверьте почту или попробуйте выполнить вход, ' \
                                       'через {time} мин.'.format(
                                                 time=(user.last_login_date + timedelta(minutes=5) - timezone.now()).seconds//60 + 1,
                                                 )
                    return render(request, 'login.html', {
                                    'name': user_name,
                                    'message': message_for_site,
                                    })

                User.objects.filter(email=email).update(last_login_date=datetime.now())
                UuidUser.objects.filter(user_uuid__email=email).update(uuid=uuid)

            except User.DoesNotExist:
                first_name = user_data.get('first_name')
                if first_name:
                    user_name = first_name
                else:
                    user_name = email.split('@')[0]
                user = User.objects.create(
                    name=user_name,
                    email=email,
                    reg_date=datetime.now(),
                    last_login_date=datetime.now(),
                )
                UuidUser.objects.create(user_uuid=user, uuid=uuid)

            message = '{name}, Вы пытаетесь выполнить вход на сайт - {site}.' \
                      'Для входа перейдите пожалуйтста по ссылке {site}/{uuid}'.format(
                                name=user_name,
                                uuid=uuid,
                                site=request.get_host(),
                                )
            message_send = EmailMessage('Login', message, to=['your@email.com'])
            message_send.send()
            message_for_site = 'На Ваш email, было отправлено сообщение с вложеной ссылкой. ' \
                               'Проверьте свою почту.'
            return render(request, 'login.html', {
                            'name': user_name,
                            'message': message_for_site,
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

    if (user.last_login_date + timedelta(minutes=1)) < timezone.now():
        message_for_site = 'Время действия ссылки истекло. Выполните повторный вход.'
        return render(request, 'login.html', {
                        'message': message_for_site,
                        'form': LoginForm(),
                        })
    message_for_site = 'Приветстуем на нашем сайте!'
    return render(request, 'login.html', {
                    'name': user.name,
                    'message': message_for_site,
                    })

