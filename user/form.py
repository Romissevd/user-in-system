from django import forms

class LoginForm(forms.Form):

    last_name = forms.CharField(
        required=False,
        max_length=30,
        label='Логин:',
    )
    email = forms.EmailField(
        label='Email:'
    )