from django.shortcuts import render

# Create your views here.

def login(request):
    name = ''
    error_message = ''
    if 'email' in request.POST:
        email = request.POST.get('email')
        if not email:
            error_message = 'Please enter your email address'
        elif '@' not in email:
            error_message = 'Invalid email!'
        else:
            name = email.split('@')[0]
    return render(request, 'login.html', {
        'name': name,
        'error': error_message,
    })

