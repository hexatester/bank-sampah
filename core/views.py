from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views import View
from .models import (
    Nasabah,
    Item,
    OrderItem,
    Order
)
from .forms import (
    UserCreateForm
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
    fields = ['name', 'addres', 'user']
    template_name = 'nasabah/add.html'


class UserUpdateView(UpdateView):
    model = Nasabah
    fields = ['name', 'addres']
    template_name = 'nasabah/detail.html'


class UserDeleteView(View):
    model = Nasabah


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

    def get(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=pk, user=request.user)
        context = {
            'head_title': obj.name,
            'object': obj
        }
        return render(request=request, template_name=self.template_name, context=context)


class ItemCreateView(CreateView):
    model = Item


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
