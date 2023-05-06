""""Shop app models.
"""
import sys
from io import BytesIO
from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import models
from django.urls import reverse
from PIL import Image


class Category(models.Model):
    """Class of category model.
    """
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        """Change this class behaviour.
        """
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        """Get absolute URL.
        """
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Size(models.Model):
    """Size class model.
    """
    name = models.CharField(max_length=5)
    description = models.TextField(blank=True)

    class Meta:
        """Change this class behaviour.
        """
        verbose_name = 'size'

    def __str__(self):
        return str(self.name)


class Product(models.Model):
    """Product model class.
    """
    category = models.ForeignKey(Category,
                                 related_name='products',
                                 on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/',
                              blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,
                                decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Change this class behaviour.
        """
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        """Get absolute URL.
        """
        return reverse('shop:product_detail',
                       args=[self.pk, self.slug])

    # before saving the instance we’re reducing the image
    def save(self, *args, **kwargs):
        if not self.pk:
            self.image = self.reduce_image_size(self.image)
        super(Product, self).save(*args, **kwargs)

    def reduce_image_size(self, picture):
        """Reduce the image size.
        """
        try:
            try:
                img = Image.open(picture)
                thumb_io = BytesIO()
                img.save(thumb_io, 'jpeg', quality=50)
            except OSError:
                img = img.convert('RGB')
                thumb_io = BytesIO()
                img.save(thumb_io, 'jpeg', quality=50)

            new_image = File(thumb_io, name=picture.name)
            thumb_io.seek(0)
            picture = InMemoryUploadedFile(
                thumb_io,
                'ImageField',
                f"{picture.name.split('.')[0]}.jpg",
                'image/jpeg',
                sys.getsizeof(thumb_io),
                None)
        except OSError:
            new_image = self.image

        return new_image
