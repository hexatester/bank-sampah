from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import (
    Nasabah,
    Item,
    OrderItem,
    Order
)

# Create your views here.

login_url = '/login'


class IndexView(View):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponseRedirect('/login')
        context = {
            'object_list': Nasabah.objects.filter(user=request.user),
            'orders': Order.objects.filter(user=request.user, ordered=False)
        }
        return render(request=request, template_name=self.template_name, context=context)


class Login(LoginView):
    template_name = 'core/login.html'
    next = '/'


class Logout(LoginRequiredMixin, LogoutView):
    login_url = login_url
    next_page = '/'

class PasswordChangeView(LoginRequiredMixin, View):
    login_url = login_url

    def get(self, request, *args, **kwargs):
        context = {
            'head_title': "Ubah Password",
            'form': PasswordChangeForm()
            }
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password berhasil dirubah!')
        context = {
            'head_title': "Ganti Password",
            'form': PasswordChangeForm()
            }
        messages.warning(request, 'Passwrd gagal dirubah')
        return render(request=request, template_name=self.template_name, context=context) 
