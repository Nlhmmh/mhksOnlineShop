from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DeleteView, DetailView, View
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.contrib import messages

from .models import Item, CategoryChoice, Order, OrderItem
from .forms import UserForm

# -----------------------------------------------------------------------------------
# User


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            print("User Registered!")
            return HttpResponseRedirect(reverse('core:login'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request, 'register.html', {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', 'a')
        password = request.POST.get('password', 'aaa')
        if username == '':
            messages.info(request, 'Please fill Username!')
            return render(request, 'login.html')
        elif password == '':
            messages.info(request, 'Please fill Password!')
            return render(request, 'login.html')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('core:home'))
            else:
                messages.info(
                    request, 'Your account is not active!')
                return render(request, 'login.html')
        else:
            messages.info(
                request, 'Your account name or password is incorrect!')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('core:home'))


@login_required
def user_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'profile.html', {"user": user})


# -----------------------------------------------------------------------------------
# Others


class HomeListView(ListView):
    model = Item
    paginate_by = 6
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryChoice.values
        context['displayCarousel'] = True
        return context


class HomeListViewByCategory(ListView):
    model = Item
    paginate_by = 6
    template_name = "index.html"

    def get(self, *args, **kwargs):
        item_list = Item.objects.filter(category=self.kwargs['category'])
        context = {
            'item_list': item_list,
            'category': self.kwargs['category'],
            'categories': CategoryChoice.values,
            'displayCarousel': False,
        }
        return render(self.request, 'index.html', context)


class AboutView(TemplateView):
    template_name = "about.html"


class ItemView(DetailView):
    model = Item
    template_name = "item.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CategoryChoice.values
        return context


# -----------------------------------------------------------------------------------
# Order


class OrderView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return render(self.request, 'order.html')


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("core:order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("core:product", slug=slug)


class CheckoutView(View):
    def get(self, *args, **kwargs):
        return render(self.request, "checkout.html")
