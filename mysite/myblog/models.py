from django.contrib.auth.models import User
from django.db import models
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    photo = models.ImageField(verbose_name=_("Photo"), upload_to="profile_pics", default="profile_pics/default.png")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)


class Post(models.Model):
    title = models.CharField(verbose_name=_("Title"), max_length=100)
    user = models.ForeignKey(to=User, verbose_name=_("Author"), on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(verbose_name=_("Date Created"), auto_now_add=True)
    content = HTMLField(verbose_name=_("Content"), max_length=10000)

    def comments_count(self):
        return self.comments.count()

    comments_count.short_description = _("Comments Count")

    class Meta:
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")
        ordering = ['-date_created']


class Comment(models.Model):
    post = models.ForeignKey(to="Post", verbose_name=_("Post"), on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(to=User, verbose_name=_("Author"), on_delete=models.CASCADE)
    date_created = models.DateTimeField(verbose_name=_("Date Created"), auto_now_add=True)
    content = models.TextField(verbose_name=_("Content"), max_length=1000)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ['-date_created']
