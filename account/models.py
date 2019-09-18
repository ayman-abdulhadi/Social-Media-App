from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.urls import reverse
from .managers import CustomUserManager
# Create your models here.


class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOISES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    username    = models.CharField(_('username'), unique=True , max_length=25)
    email       = models.EmailField(_('email address'), unique=True)
    first_name  = models.CharField(_('first name'), blank=True, max_length=30)
    last_name   = models.CharField(_('last name'), blank=True, max_length=30)
    join_date   = models.DateTimeField(blank=True, default=timezone.now)
    is_active   = models.BooleanField(default=True)
    is_staff    = models.BooleanField(default=False)
    is_superuser= models.BooleanField(default=False)
    birth_date  = models.DateField(_('birth date'), default=timezone.localdate)
    gender      = models.CharField(_('gender'), choices=GENDER_CHOISES, default='male', max_length=10)
    avatar      = models.FileField(upload_to="avatars/", blank=True, default='avatars/default.png')

    objects     = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_absolute_url(self):
        return reverse('account:user_detail', args=[self.username])

    def __str__(self):
        return self.email


class Contact(models.Model):
    user_from = models.ForeignKey(CustomUserModel, related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey(CustomUserModel, related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{} follows {}'.format(self.user_from, self.user_to)

CustomUserModel.add_to_class('following',models.ManyToManyField('self', through=Contact,
                                related_name='followers', symmetrical=False))
