from django import forms
from django.contrib.auth.forms import UserCreationForm ,UsernameField , AuthenticationForm
from django.contrib.auth import password_validation
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget= forms.TextInput(attrs={'class' : 'form-control'})
    )
  
    email = forms.EmailField(
        widget= forms.EmailInput(attrs={'class' : 'form-control'})
    )
 
    password1 = forms.CharField(
        label= ("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class' : 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label= ("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class' : 'form-control'}),
        strip=False,
        help_text= ("Enter the same password as before, for verification."),
    )

    class Meta:
        model = User
        fields = ("username","email")
        field_classes = {"username": UsernameField}
    
    error_messages = {
        "password_mismatch": ("The two password fields didn't match."),
    }
 

class SignInForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={"autofocus": True , "class":"form-control"}))
    password = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password","class":"form-control"}),
    )

    error_messages = {
        "invalid_login": (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": ("This account is inactive."),
    }