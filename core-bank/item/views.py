from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from item.models import Item
from .forms import (
    ItemCreateForm
)

# Create your views here.


class BaseView(LoginRequiredMixin):
    name = ""
    login_url = '/login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = self.name
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class ItemListView(BaseView, ListView):
    name = 'Barang'
    model = Item
    template_name = 'item/index.html'
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.order_by('pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = Item.objects.filter(user=self.request.user).count()
        return context


class ItemUpdateView(BaseView, SuccessMessageMixin, UpdateView):
    name = 'Edit Barang'
    model = Item
    form_class = ItemCreateForm
    template_name = 'item/detail.html'
    success_message = 'Barang "%(name)s" berhasil diupdate'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Edit Barang - {}'.format(
            context.get('object'))
        return context


class ItemCreateView(BaseView, SuccessMessageMixin, CreateView):
    model = Item
    form_class = ItemCreateForm
    template_name = 'item/create.html'
    success_message = 'Barang "%(name)s" berhasil ditambahkan'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class ItemDeleteView(BaseView, SuccessMessageMixin, DeleteView):
    nama = "Hapus Barang"
    model = Item
    template_name = 'item/delete.html'
    success_message = 'Barang "%(name)s" berhasil dihapus'
    success_url = '/item'
