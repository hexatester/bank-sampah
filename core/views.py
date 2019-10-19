from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.views import View
from .models import (
    Nasabah,
    Item,
    OrderItem,
    Order
)
from .forms import (
    NasabahCreateForm,
    ItemCreateForm,
    OrderItemCreateForm
)

# Create your views here.


def index(request):
    return render(request=request, template_name='core/index.html')

def logout_view(request):
    pass

class IndexView(View):
    template_name = 'core/index.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return HttpResponseRedirect('/login')
        context = {
            'nasabah_list': Nasabah.objects.filter(user=request.user),
            'orders': Order.objects.filter(user=request.user)
        }
        return render(request=request, template_name=self.template_name, context=context)


class Login(LoginView):
    template_name = 'core/login.html'
    next = '/'

class Logout(LogoutView):
    next_page = '/'
    

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
            return HttpResponseRedirect(reverse("core:item", kwargs={
                'pk': item.pk
            }))
        context = {
            'form': form
        }
        # Messages sucess creating item
        return render(request=request, template_name=self.template_name, context=context)


class ItemDeleteView(DeleteView):
    model = Item
    template_name = 'item/delete.html'
    success_url = '/items'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.user = self.request.user
        obj.save()
        return obj


class OrderListView(ListView):
    model = Order
    template_name = 'order/index.html'

    def get(self, request, *args, **kwargs):
        context = {
            'head_title': 'Daftar Transaksi',
            'object_list': self.model.objects.filter(user=request.user)
        }
        return render(request=request, template_name=self.template_name, context=context)


class OrderItemView(View):
    template_name = ''

    def get(self, request, pk, *args, **kwargs):
        nasabah = get_object_or_404(Nasabah, pk=pk, user=request.user)
        order = get_object_or_404(
            Order, user=request.user, nasabah=nasabah, ordered=False)
        context = {
            'order': order
        }
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, pk, *args, **kwargs):
        nasabah = get_object_or_404(Nasabah, pk=pk, user=request.user)
        order = get_object_or_404(
            Order, user=request.user, nasabah=nasabah, ordered=False)
        context = {
            'order': order,
            'nasabah': nasabah,
            'items': Item.objects.filter(user=request.user)
        }
        return render(request=request, template_name=self.template_name, context=context)


class OrderCreateView(View):
    model = Order
    template_name = 'order/index.html'
    form_class = OrderItemCreateForm

    def get(self, request, pk, *args, **kwargs):
        nasabah = get_object_or_404(Nasabah, pk=pk, user=request.user)
        orders, created = Order.objects.get_or_create(
            user=request.user, nasabah=nasabah, ordered=False
        )
        context = {
            'form': OrderItemCreateForm(user=request.user)
        }
        if not created:
            context['order'] = orders
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, pk, *args, **kwargs):
        nasabah = get_object_or_404(Nasabah, pk=pk, user=request.user)
        if self.autos(request, nasabah):
            return HttpResponseRedirect(nasabah.get_order_url())
        return HttpResponseRedirect(nasabah.get_order_url())

    def autos(self, request, nasabah):
        form = self.form_class(request.POST, user=request.user)
        if not form.is_valid():
            return False
        order_item = form.save(commit=False)
        order_item.nasabah = nasabah
        order_item.user = request.user
        order_item.save()
        orders, created = Order.objects.get_or_create(
            user=request.user, nasabah=nasabah, ordered=False
        )
        if created:
            orders.save()
        orders.items.add(order_item)
        orders.save()
        return True


class OrderDeleteView(DeleteView):
    model = Order
    template_name = 'order/delete.html'
    success_url = '/users'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        obj.user = self.request.user
        obj.save()
        return obj
