from django.db import models
from garpix_page.models import BasePage
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


class ApiPage(BasePage):
    template = "pages/api.html"

    class Meta:
        verbose_name = "Api"
        verbose_name_plural = "Apis"
        ordering = ("-created_at",)


def validate_file_size(value):
    filesize = value.size
    if filesize > 5242880:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")
    else:
        return value


class Album(models.Model):
    title = models.CharField(max_length=70)
    description = models.TextField(max_length=1024)
    is_visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class AlbumImage(models.Model):
    name = models.CharField(max_length=70)
    pic = models.FileField(verbose_name='Image',
                           validators=[validate_file_size,
                                       FileExtensionValidator(['jpg', 'jpeg', 'png'])],
                           blank=True)
    thumb = ImageSpecField(source='pic', processors=[ResizeToFit(150)])
    created = models.DateTimeField(auto_now_add=True)
    album = models.ForeignKey(Album, related_name='photos', on_delete=models.CASCADE)
    tags = models.CharField(max_length=250)
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
