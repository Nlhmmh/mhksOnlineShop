from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django_resized import ResizedImageField


# CATEGORY_CHOICES = (
#     ('shirt', 'Shirt'),
#     ('trousers', 'Trousers'),
#     ('skirt', 'Skirt'),
#     ('outwear', 'Outwear'),
# )

# GENDER_CHOICES = (
#     ('M', 'Male'),
#     ('F', 'Female'),
# )


# Create your models here.
class CategoryChoice(models.TextChoices):
    clothing = 'Clothing'
    beauty = 'Beauty'
    jewellery = 'Jewellery'
    bags = 'Bags'
    shoes = 'Shoes'


class GenderChoice(models.TextChoices):
    male = 'Male'
    female = 'Female'
    both = 'both'


class RatingChoice(models.TextChoices):
    zero = 'zero'
    one = 'one'
    two = 'two'
    three = 'three'
    four = 'four'
    five = 'five'


class Item(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    category = models.CharField(choices=CategoryChoice.choices, max_length=20)
    gender = models.CharField(
        choices=GenderChoice.choices,
        max_length=20,
        default='both',
        null=True
    )
    stock = models.IntegerField()
    description = models.TextField()
    image = ResizedImageField(
        size=[700, 600],
        quality=99,
        crop=['middle', 'center'],
        upload_to='images'
    )
    slug = models.SlugField(null=False, unique=True)
    rating = models.CharField(
        choices=RatingChoice.choices,
        max_length=20,
        null=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("core:item", kwargs={
            'slug': self.slug
        })

    def check_stock(self):
        if self.stock > 0:
            isInStock = 'In Stock'
        else:
            isInStock = 'Out Of Stock'
        return isInStock

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return "User \"" + self.user.username + "\" ordered  " + self.item.name

    def get_total_item_price(self):
        return self.quantity * self.item.price


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)

    def __str__(self):
        return "Order of User " + self.user.username + ""

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_item_price()
        # if self.coupon:
        #     total -= self.coupon.amount
        return total
