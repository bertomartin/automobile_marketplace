from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from web_client.models import *


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Last Name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repeat password'})

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class OfferForm(forms.ModelForm):

    make = forms.ModelChoiceField(queryset=Manufacturer.objects.all())
    engine_type = forms.ModelChoiceField(queryset=EngineType.objects.all())
    engine_capacity = forms.ModelChoiceField(queryset=EngineCapacity.objects.all())
    body_type = forms.ModelChoiceField(queryset=BodyType.objects.all())

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        self.fields['make'].widget.attrs.update({'class': 'form-control'})
        self.fields['model'].widget.attrs.update({'class': 'form-control'})
        self.fields['engine_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['engine_capacity'].widget.attrs.update({'class': 'form-control'})
        self.fields['body_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['production_year'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Additional description'})
        self.fields['price'].widget.attrs.update({'class': 'form-control'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Offer
        fields = ['make', 'model', 'engine_type', 'engine_capacity', 'body_type', 'production_year', 'description', 'price', 'phone_number']
