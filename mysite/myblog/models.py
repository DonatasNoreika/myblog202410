from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Post(models.Model):
    title = models.CharField(verbose_name="Pavadinimas", max_length=100)
    user = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    content = models.TextField(verbose_name="Tekstas", max_length=10000)


class Comment(models.Model):
    post = models.ForeignKey(to="Post", verbose_name="Įrašas", on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    content = models.TextField(verbose_name="Tekstas", max_length=1000)
