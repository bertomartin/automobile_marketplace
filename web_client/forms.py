from django import forms
from django.contrib.auth.forms import UserCreationForm
from web_client.models import *
from django.db import transaction


class CustomerSignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomerSignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Username'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repeat password'})

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_customer = True
        user.save()
        CustomerModel.objects.create(user=user)
        return user


class UpdateCustomerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateCustomerForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = CustomerModel
        fields = ['name', 'email', 'phone_number']


class ContractorSignUpForm(UserCreationForm):

    # title = forms.CharField(max_length=20, required=True)

    def __init__(self, *args, **kwargs):
        super(ContractorSignUpForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_contractor = True
        user.save()
        contractor = ContractorModel.objects.create(user=user)
        # contractor.title = (self.cleaned_data.get('title'))
        contractor.save()
        return user


class UpdateContractorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateContractorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = ContractorModel
        fields = ['title', 'street', 'city', 'country', 'email', 'phone_number', 'status']


class OfferForm(forms.ModelForm):

    make = forms.ModelChoiceField(queryset=Manufacturer.objects.all())
    engine_type = forms.ModelChoiceField(queryset=EngineType.objects.all())
    engine_capacity = forms.ModelChoiceField(queryset=EngineCapacity.objects.all())
    body_type = forms.ModelChoiceField(queryset=BodyType.objects.all())

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Additional description'})

    class Meta:
        model = Post
        fields = ['make', 'model', 'engine_type', 'engine_capacity', 'body_type', 'production_year', 'description', 'price', 'phone_number', 'contact_person']
