from io import BytesIO
from django.core.files import File
from django.db import models
from django.urls import reverse
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])


class Size(models.Model):
    name = models.CharField(max_length=5)
    description = models.TextField(blank=True)


    class Meta:
        verbose_name = 'size'

    def __str__(self):
        return str(self.name)


class Product(models.Model):
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
        ordering = ['name']
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['name']),
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])

    # before saving the instance we’re reducing the image
    def save(self, *args, **kwargs):
        new_image = self.reduce_image_size(self.image)
        self.image = new_image
        super().save(*args, **kwargs)

    def reduce_image_size(self, profile_pic):
        print(profile_pic)
        img = Image.open(profile_pic)
        thumb_io = BytesIO()
        img.save(thumb_io, 'jpeg', quality=50)
        new_image = File(thumb_io, name=profile_pic.name)
        return new_image
