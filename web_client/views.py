from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import View
from web_client.forms import UserForm


class UserFormView(View):
    template_name = 'auth/auth.html'

    def get(self, request):
        form = UserForm(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']

            # properly set/change password
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('homepage')

        return render(request, self.template_name, {'form': form})


class Homepage(View):
    template_name = 'homepage/index.html'

    def get(self, request):
        return render(request, self.template_name, {'testval': self.template_name})
