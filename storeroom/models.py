from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError


class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    price = models.IntegerField()
    available = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('storeroom:storeroom_detail', args=[self.name, ])

    def clean(self):
        if self.available<0:
            raise ValidationError('availability not enough')