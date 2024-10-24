from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField
from PIL import Image

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name="Nuotrauka", upload_to="profile_pics", default="profile_pics/default.png")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)


class Post(models.Model):
    title = models.CharField(verbose_name="Pavadinimas", max_length=100)
    user = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    content = HTMLField(verbose_name="Tekstas", max_length=10000)

    def comments_count(self):
        return self.comments.count()

    class Meta:
        verbose_name = 'Įrašas'
        verbose_name_plural = 'Įrašai'
        ordering = ['-date_created']


class Comment(models.Model):
    post = models.ForeignKey(to="Post", verbose_name="Įrašas", on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(to=User, verbose_name="Autorius", on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name="Data", auto_now_add=True)
    content = models.TextField(verbose_name="Tekstas", max_length=1000)

    class Meta:
        verbose_name = 'Komentaras'
        verbose_name_plural = 'Komentarai'
        ordering = ['-date_created']
