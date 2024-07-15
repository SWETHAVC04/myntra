from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100)
    aesthetic = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()

    def __str__(self):
        return self.name

class UserPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    preferred_aesthetics = models.JSONField(default=list)

    def __str__(self):
        return f"{self.user.username}'s preferences"

# We'll comment out the Outfit model for now as it's not being used
# class Outfit(models.Model):
#     items = models.ManyToManyField(Item)
#     aesthetic = models.CharField(max_length=100)
#
#     def __str__(self):
#         return f"Outfit {self.id}"