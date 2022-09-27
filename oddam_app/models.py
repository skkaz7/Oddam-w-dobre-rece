from django.db import models
from django.contrib.auth.models import User

# Create your models here.

TYPE = (
    (1, 'Fundacja'),
    (2, 'Organizacja pozarządowa'),
    (3, 'Zbiórka lokalna')
)


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Institution(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    type = models.IntegerField(choices=TYPE, default=TYPE[0])
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.name


class Donation(models.Model):
    quantity = models.IntegerField()
    categories = models.ManyToManyField(Category)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    address = models.TextField(max_length=64)
    phone_number = models.IntegerField()
    city = models.CharField(max_length=64)
    zip_code = models.CharField(max_length=16)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    pick_up_comment = models.TextField()
    user = models.ForeignKey(User, null=True, default=None, on_delete=models.CASCADE)
    is_taken = models.BooleanField(default=False)
