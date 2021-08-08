from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.



STATE_CHOICES = (
    ('Andaman & Nicobar Islands', 'Andaman & Nicobar Islands',),
    ('Andhra Pradesh', 'Andhra Pradesh'),
    ('Assam', 'Assam'),
    ('Bihar', 'Bihar'),
    ('Rajeshthan', 'Rajeshthan'),
    ('Madhya Pradesh', 'Madhya Pradesh'),
    ('Utter Pradesh', 'Utter Pradesh'),
    ('Hariyana', 'Hariyana'),
    ('Punjab', 'Punjab'),
    ('Maharashtra', 'Maharashtra'),
    ('Goa', 'Goa'),
    ('Delhi', 'Delhi'),
    ('Gujarat', 'Gujarat'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES  = (
    ('P', 'Protein'),
    ('M', 'Medicine'),
    ('S', 'Syrups'),
    ('T', 'Tube'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='productimg')
    # product_offer1 = models.TextField()
    # product_offer2 = models.TextField()
    # product_info1 = models.TextField()
    # product_info2 = models.TextField()

    def __str__(self):
        return str(self.id)


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    totalamount = models.FloatField(default=0)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    totalamount = models.FloatField(default=0)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price



