from django.urls import reverse_lazy, reverse
from django.views import generic
from django.shortcuts import render
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.db import close_old_connections


class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm  # variables must be underscores
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def profile(request, username):
    close_old_connections()
    player = CustomUser.objects.get(username=username)
    context = {
        'player': player
    }
    close_old_connections()
    return render(request, 'profile.html', context)


class Edit(generic.UpdateView):
    model = CustomUser
    template_name = 'edit.html'
    slug_field = 'id'
    fields = ['avatar']
