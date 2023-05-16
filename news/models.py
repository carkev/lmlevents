"""News models module.
"""
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from tinymce.models import HTMLField
from .fields import OrderField


class Subject(models.Model):
    """Subjects class model.
    """
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        """Change this class behaviour.
        """
        ordering = ['title']

    def __str__(self):
        return str(self.title)


class News(models.Model):
    """News class model.
    """
    owner = models.ForeignKey(User,
                              related_name='news_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='news',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Change this class behaviour.
        """
        verbose_name_plural = 'news'
        ordering = ['-created']

    def __str__(self):
        return str(self.title)


class Module(models.Model):
    """Module class model.
    """
    news = models.ForeignKey(News,
                             related_name='modules',
                             on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['news'])

    class Meta:
        """Change this class behaviour.
        """
        ordering = ['order']

    def __str__(self):
        return f'{self.order}. {self.title}'


class Content(models.Model):
    """Content class model.
    """
    module = models.ForeignKey(Module,
                               related_name='contents',
                               on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType,
                                     on_delete=models.CASCADE,
                                     limit_choices_to={'model__in': (
                                         'text',
                                         'video',
                                         'image',
                                         'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        """Change this class behaviour.
        """
        ordering = ['order']


class ItemBase(models.Model):
    """ItemBase class model.
    """
    owner = models.ForeignKey(User,
                              related_name='%(class)s_related',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        """Change this class behaviour.
        """
        abstract = True

    def __str__(self):
        return str(self.title)

    def render(self):
        """Return the HTML file name to get the template.
        """
        return render_to_string(
            f'news/content/{self._meta.model_name}.html',
            {'item': self})


class Text(ItemBase):
    """Text class model.
    """
    content = HTMLField()


class File(ItemBase):
    """File class model.
    """
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    """Image class model.
    """
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    """Video class model.
    """
    url = models.URLField()
