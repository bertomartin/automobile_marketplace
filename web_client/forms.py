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
        Customer.objects.create(user=user)
        return user


class UpdateCustomerForm(forms.ModelForm):

    name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super(UpdateCustomerForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone_number']


class ContractorSignUpForm(UserCreationForm):

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
        contractor = Contractor.objects.create(user=user)
        contractor.save()
        return user


class UpdateContractorForm(forms.ModelForm):

    status = forms.BooleanField(label='Active status', required=False)

    def __init__(self, *args, **kwargs):
        super(UpdateContractorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Contractor
        fields = ['title', 'street', 'city', 'country', 'email', 'phone_number', 'status']


class OfferForm(forms.ModelForm):

    make = forms.ModelChoiceField(label='Manufacturer', queryset=Manufacturer.objects.all())
    engine_type = forms.ModelChoiceField(label='Engine', queryset=EngineType.objects.all())
    engine_capacity = forms.ModelChoiceField(label='Capacity', queryset=EngineCapacity.objects.all())
    body_type = forms.ModelChoiceField(queryset=BodyType.objects.all())

    def __init__(self, *args, **kwargs):
        super(OfferForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'placeholder': 'Additional description'})
        self.fields['make'].widget.attrs.update({'text': 'Manufacturer'})
        self.fields['model'].queryset = Series.objects.none()

        if 'make' in self.data:
            try:
                manufacturer_id = int(self.data.get('make'))
                self.fields['model'].queryset = Series.objects.filter(make_fk=manufacturer_id).order_by('series')
            except ValueError:
                pass  # invalid input from the client; ignore and fallback to empty City queryset

    class Meta:
        model = Post
        fields = ['make', 'model', 'engine_type', 'engine_capacity', 'body_type', 'production_year', 'description', 'price', 'phone_number', 'contact_person']


class ImageForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ImageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Image
        fields = ('image',)


class SearchForm(forms.Form):

    make = forms.ModelChoiceField(label='Manufacturer', queryset=Manufacturer.objects.all(), required=False)
    engine_type = forms.ModelChoiceField(label='Engine', queryset=EngineType.objects.all(), required=False)
    engine_capacity = forms.ModelChoiceField(label='Capacity', queryset=EngineCapacity.objects.all(), required=False)
    body_type = forms.ModelChoiceField(queryset=BodyType.objects.all(), required=False)
    price_bottom = forms.IntegerField(min_value=1, required=False)
    price_top = forms.IntegerField(max_value=10000000, required=False)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        fields = ['make', 'engine_type', 'engine_capacity', 'body_type', 'price_bottom', 'price_top']