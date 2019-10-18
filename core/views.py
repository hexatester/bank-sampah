from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views import View
from .models import (
    Nasabah,
    Item,
    OrderItem,
    Order
)
from .forms import (
    NasabahCreateForm,
    ItemCreateForm
)

# Create your views here.


def index(request):
    return render(request=request, template_name='core/index.html')


@login_required
def nasabah_list_view(request):
    context = {
        'items': Nasabah.objects.get(user=request.user)
    }
    return render(request=request, template_name='nasabah/index.html', context=context)


class UserListView(ListView):
    model = Nasabah
    template_name = 'nasabah/index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'head_title': 'Nasabah',
            'object_list': self.model.objects.filter(user=request.user)
        }
        return render(request=request, template_name=self.template_name, context=context)


class UserCreateView(CreateView):
    model = Nasabah
    form_class = NasabahCreateForm
    template_name = 'nasabah/create.html'

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.form_class()
        }
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            nasabah = form.save(commit=False)
            nasabah.user = request.user
            nasabah.save()
            return HttpResponseRedirect(reverse("core:user", kwargs={
                'pk': nasabah.pk
            }))
        context = {
            'form': form
        }
        return render(request=request, template_name=self.template_name, context=context)


class UserUpdateView(UpdateView):
    model = Nasabah
    fields = ['name', 'addres']
    template_name = 'nasabah/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.user = self.request.user
        obj.save()
        return obj


class UserDeleteView(DeleteView):
    model = Nasabah
    template_name = 'nasabah/delete.html'
    success_url = '/users'


class ItemListView(ListView):
    model = Item
    template_name = 'item/index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'head_title': 'Barang',
            'object_list': self.model.objects.filter(user=request.user)
        }
        return render(request=request, template_name=self.template_name, context=context)


class ItemUpdateView(UpdateView):
    model = Item
    fields = ['name', 'price']
    template_name = 'item/detail.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.user = self.request.user
        obj.save()
        return obj


class ItemCreateView(CreateView):
    model = Item
    form_class = ItemCreateForm
    template_name = 'item/create.html'

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
            return HttpResponseRedirect(reverse("core:user", kwargs={
                'pk': item.pk
            }))
        context = {
            'form': form
        }
        return render(request=request, template_name=self.template_name, context=context)


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'item/delete.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.user = self.request.user
        obj.save()
        return obj


def order(request, pk):
    nasabah = get_object_or_404(Nasabah, pk=pk, user=request.user)
    order, created = Order.objects.get_or_create(
        user=request.user, nasabah=nasabah, ordered=False)
    context = {
        'order': order,
        'nasabah': nasabah,
        'items': Item.objects.filter(user=request.user)
    }
    return render(request=request, template_name='order/index.html')
