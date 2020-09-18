from django.urls import path
from .views import (
    register,
    user_login,
    user_logout,
    user_profile,
    HomeListView,
    AboutView,
    ItemView,
    OrderView,
    HomeListViewByCategory,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    CheckoutView,
)

app_name = 'core'

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('category/<category>/',
         HomeListViewByCategory.as_view(), name='homeByCategory'),
    path('about/', AboutView.as_view(), name='about'),
    path('item/<slug>/', ItemView.as_view(), name='item'),

    path('register/', register, name='register'),
    path('user_login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('user/profile/<username>/',
         user_profile, name='profile'),

    path('order-summary/', OrderView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),

    path('checkout/', CheckoutView.as_view(), name='checkout'),
]
