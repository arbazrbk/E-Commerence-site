from django import forms
from .models import Customer, Product
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm


class Registrationforms(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'zipcode']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control' }),
            'locality': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 400px;'}),
            'state': forms.Select(attrs={'class': 'form-control', 'style': 'width: 400px;'}),

        }    


class Loginforms(AuthenticationForm):
    pass


class ChangePasswordForm(PasswordChangeForm):
    pass


class ResetPasswordForm(PasswordResetForm):
    pass