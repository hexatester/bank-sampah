from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib import messages, humanize
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
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


class BaseView(LoginRequiredMixin):
    name = ''
    login_url = '/login'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = self.name
        return context

    def render(self, context: dict, *args, **kwargs):
        return render(request=self.request, template_name=self.template_name, context=context, *args, **kwargs)


class UserListView(BaseView, ListView):
    name = 'Nasabah'
    model = Nasabah
    template_name = 'nasabah/index.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('pk')


class UserCreateView(BaseView, SuccessMessageMixin, CreateView):
    name = 'Tambah Nasabah'
    model = Nasabah
    form_class = NasabahCreateForm
    success_message = 'Nasabah %(name)s berhasil ditambahkan'
    template_name = 'nasabah/create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UserUpdateView(BaseView, SuccessMessageMixin, UpdateView):
    name = 'Update Nasabah'
    model = Nasabah
    form_class = NasabahCreateForm
    success_message = 'Perubahan data nasabah %(name)s disimpan'
    template_name = 'nasabah/detail.html'


class UserDeleteView(BaseView, SuccessMessageMixin, DeleteView):
    name = 'Hapus Nasabah'
    model = Nasabah
    success_message = 'Nasabah %(name)s berhasil dihapus'
    template_name = 'nasabah/delete.html'
    success_url = '/nasabah'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Edit Nasabah - {}'.format(
            context['object'].name)
        return context


class WithdrawView(BaseView, View):
    model = Nasabah
    template_name = 'nasabah/withdraw.html'
    forms = WithdrawForm

    def get(self, request, pk, *args, **kwargs):
        context = {
            'head_title': 'Kurangi Saldo',
            'nasabah': get_object_or_404(Nasabah, pk=pk, user=request.user),
            'form': self.forms()
        }
        return self.render(context=context)

    def post(self, request, pk, *args, **kwargs):
        nasabah = get_object_or_404(Nasabah, pk=pk, user=request.user)
        form = self.forms(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('value') <= nasabah.balance:
                val = form.cleaned_data.get('value')
                nasabah.balance -= val
                nasabah.save()
                messages.success(
                    request, f'Saldo {nasabah.name} berhasil dikurangi sebesar Rp {val}')
            else:
                messages.warning(
                    request, f'Saldo {nasabah.name} tidak mencukupi')
        context = {
            'head_title': 'Kurangi Saldo',
            'nasabah': nasabah,
            'form': self.forms()
        }
        return self.render(context=context)
