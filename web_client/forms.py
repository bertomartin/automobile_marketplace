from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    # def __init__(self, *args, **kwargs):
    #     super(UserForm, self).__init__(*args, **kwargs)
    #     self.fields['csv_file'].widget.attrs.update({'class': 'btn btn-default', 'role': 'button'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
