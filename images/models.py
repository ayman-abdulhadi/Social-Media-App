from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey

# Create your models here.

class Comment(models.Model):
    content_type   = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    user    = models.ForeignKey(settings.AUTH_USER_MODEL, null=True ,related_name='users_comment', on_delete=models.CASCADE)
    body    = models.CharField(max_length=512, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created',]

    def __str__(self):
        return 'Comment by {} on {}'.format(self.user, "test")

class Image(models.Model):
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='images_created', on_delete=models.CASCADE)
    title          = models.CharField(max_length=100)
    slug           = models.SlugField(blank=True, max_length=200)
    url            = models.URLField(blank=True)
    image          = models.ImageField(upload_to='images/%Y/%m/%d/', blank=True)
    body           = models.TextField(blank=True)
    created        = models.DateField(auto_now_add=True, db_index=True)
    users_like     = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='images_liked', blank=True)
    total_likes    = models.PositiveIntegerField(db_index=True, default=0)
    comments       = GenericRelation(Comment, blank=True, null=True)

    class Meta:
        ordering = ['-created',]

    def __str__(self):
        return self.title

    def published():
        now = timezone.now()
        last_minute = now - datetime.timedelta(seconds=60)
        return last_minute

    def get_absolute_url(self):
        return reverse('images:detail', args=[self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image, self).save(*args, **kwargs)
