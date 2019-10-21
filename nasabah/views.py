from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from core.models import (
    Nasabah,
    Item,
    OrderItem,
    Order
)
from .forms import (
    NasabahCreateForm,
    WithdrawForm
)
# Create your views here.


class UserListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Nasabah
    template_name = 'nasabah/index.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset.order_by('pk')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Nasabah'
        return context


class UserCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login'
    model = Nasabah
    form_class = NasabahCreateForm
    template_name = 'nasabah/create.html'

    def get(self, request, *args, **kwargs):
        context = {
            'head_title': 'Tambah nasabah',
            'form': self.form_class()
        }
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nasabah = form.save(commit=False)
            nasabah.user = request.user
            nasabah.save()
            return HttpResponseRedirect(reverse("nasabah:view", kwargs={
                'pk': nasabah.pk
            }))
        context = {
            'form': form
        }
        return render(request=request, template_name=self.template_name, context=context)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Nasabah
    fields = ['name', 'addres']
    template_name = 'nasabah/detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Edit Nasabah - {}'.format(
            context['object'].name)
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = Nasabah
    template_name = 'nasabah/delete.html'
    success_url = '/nasabah'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Edit Nasabah - {}'.format(
            context['object'].name)
        return context


class WithdrawView(LoginRequiredMixin, View):
    login_url = '/login'
    model = Nasabah
    template_name = 'nasabah/withdraw.html'
    forms = WithdrawForm

    def get(self, request, pk, *args, **kwargs):
        context = {
            'head_title': 'Kurangi Saldo',
            'nasabah': get_object_or_404(Nasabah, pk=pk, user=request.user),
            'form': self.forms()
        }
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, pk, *args, **kwargs):
        nasabah = get_object_or_404(Nasabah, pk=pk, user=request.user)
        form = self.forms(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('value') <= nasabah.balance:
                nasabah.balance -= form.cleaned_data.get('value')
                nasabah.save()
        context = {
            'head_title': 'Kurangi Saldo',
            'nasabah': nasabah,
            'form': self.forms()
        }
        return render(request=request, template_name=self.template_name, context=context)

