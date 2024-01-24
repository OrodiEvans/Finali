from django.db import models


# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username


class Product(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product_images/')

    def __str__(self):
        return self.name


