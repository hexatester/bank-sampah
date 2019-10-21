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
from .forms import (
    NasabahCreateForm,
    ItemCreateForm,
    OrderItemCreateForm,
    OrderSubmitForm,
    WithdrawForm
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
            return HttpResponseRedirect(reverse("core:user", kwargs={
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
    success_url = '/users'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Edit Nasabah - {}'.format(
            context['object'].name)
        return context


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


class ItemUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    model = Item
    fields = ['name', 'price']
    template_name = 'item/detail.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Edit Barang - {}'.format(
            context.get('object'))
        return context


class ItemCreateView(LoginRequiredMixin, View):
    login_url = '/login'
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


class ItemDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = Item
    template_name = 'item/delete.html'
    success_url = '/items'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = '{} | Hapus Barang'.format(context.get('object'))
        return context


class OrderListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    template_name = 'order/index.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Penimbangan'
        return context


class OrderItemView(LoginRequiredMixin, View):
    login_url = '/login'
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Penimbangan'
        return context


class OrderCreateView(LoginRequiredMixin, View):
    login_url = '/login'
    model = Order
    template_name = 'order/create.html'
    form_class = OrderItemCreateForm

    def get(self, request, pk, *args, **kwargs):
        nasabah = get_object_or_404(Nasabah, pk=pk, user=request.user)
        orders, created = Order.objects.get_or_create(
            user=request.user, nasabah=nasabah, ordered=False
        )
        if request.GET.get('update'):
            order_item = get_object_or_404(OrderItem, pk=request.GET.get(
                'update'), nasabah=nasabah, user=request.user)
            form = OrderItemCreateForm(instance=order_item, user=request.user)
        elif request.GET.get('delete'):
            order_item = get_object_or_404(OrderItem, pk=request.GET.get(
                'delete'), nasabah=nasabah, user=request.user)
            order_item.delete()
            form = OrderItemCreateForm(user=request.user)
        else:
            form = OrderItemCreateForm(user=request.user)
        context = {
            'head_title': 'Penimbangan',
            'form': form
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


class OrderDeleteView(LoginRequiredMixin, DeleteView):
    login_url = '/login'
    model = Order
    template_name = 'order/delete.html'
    success_url = '/users'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Hapus Order - {}'.format(context.get('nasabah'))
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class OrderSubmitView(LoginRequiredMixin, View):
    login_url = '/login'
    template_name = 'order/submit.html'

    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        context = {
            'form': OrderSubmitForm()
        }
        return render(request=request, template_name=self.template_name, context=context)

    def post(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        form = OrderSubmitForm(request.POST, instance=order)
        if form.is_valid():
            if form.cleaned_data['sums']:
                order = form.save(commit=False)
                order.ordered = True
                nasabah = order.nasabah
                nasabah.add_balance(order.get_sum())
                nasabah.save()
            else:
                order.total = order.get_sum()
            order.save()
        return HttpResponseRedirect('/')


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
