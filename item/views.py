from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from core.models import (
    Nasabah,
    Item,
    OrderItem,
    Order
)
from .forms import (
    ItemCreateForm
)

# Create your views here.


class ItemListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Item
    template_name = 'item/index.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset.order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Barang'
        return context


class ItemUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = '/login'
    model = Item
    form_class = ItemCreateForm
    template_name = 'item/detail.html'
    success_message = 'Barang "%(name)s" berhasil diupdate'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Edit Barang - {}'.format(
            context.get('object'))
        return context


class ItemCreateView(LoginRequiredMixin, SuccessMessageMixin, View):
    login_url = '/login'
    model = Item
    form_class = ItemCreateForm
    template_name = 'item/create.html'
    success_message = 'Barang "%(name)s" berhasil ditambahkan'

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class()
        }
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            return HttpResponseRedirect(reverse("item:view", kwargs={
                'pk': item.pk
            }))
        context = {
            'form': form
        }
        # Messages sucess creating item
        return render(request=request, template_name=self.template_name, context=context)


class ItemDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = '/login'
    model = Item
    template_name = 'item/delete.html'
    success_message = 'Barang "%(name)s" berhasil dihapus'
    success_url = '/item'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = '{} | Hapus Barang'.format(
            context.get('object'))
        return context
