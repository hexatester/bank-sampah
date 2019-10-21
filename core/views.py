from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from .models import (
    Nasabah,
    Item,
    OrderItem,
    Order
)

# Create your views here.


class IndexView(View):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponseRedirect('/login')
        context = {
            'nasabah_list': Nasabah.objects.filter(user=request.user),
            'orders': Order.objects.filter(user=request.user, ordered=False)
        }
        return render(request=request, template_name=self.template_name, context=context)


class Login(LoginView):
    template_name = 'core/login.html'
    next = '/'


class Logout(LoginRequiredMixin, LogoutView):
    login_url = '/login'
    next_page = '/'
