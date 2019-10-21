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
    OrderItemCreateForm,
    OrderSubmitForm,
)

# Create your views here.


class OrderListView(LoginRequiredMixin, ListView):
    login_url = '/login'
    model = Order
    template_name = 'order/index.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset.queryset.order_by('pk')

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
        messages.success(request, f'Penimbangan "{order_item}" berhasil ditambahkan')
        return True


class OrderDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    login_url = '/login'
    model = Order
    success_message = 'Penimbangan %(nasabah)s dihapus'
    template_name = 'order/delete.html'
    success_url = '/nasabah'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['head_title'] = 'Hapus Order - {}'.format(
            context.get('nasabah'))
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
            order = form.save(commit=False)
            if form.cleaned_data['sums']:
                order.ordered, order.total = True, order.get_sum()
                nasabah = order.nasabah
                nasabah.add_balance(order.get_sum())
                nasabah.save()
                messages.success(request, f'Saldo {nasabah} berhasil ditambah Rp. {order.get_sum()}')
            else:
                order.total = order.get_sum()
            order.save()
        return HttpResponseRedirect('/')

