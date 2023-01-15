from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser


from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


    def get_short_name(self):
        return self.username


    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Order(models.Model):
    CHOICES = (
        ('Отправлен', 'Отправлен'),
        ('Отказ', 'Отказ'),
        ('Скоро свяжемся', 'Скоро свяжемся'),
        ('Принят в работу', 'Принят в работу'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_done = models.BooleanField(default=False)
    status = models.CharField(max_length=50, choices=CHOICES, null=True)
    # cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    personal_info = models.TextField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", null=True, blank=True, verbose_name="Фото")

    def __str__(self):
        return str(self.user)

    def get_age(self):
        import datetime

        return  f'birthday: {self.birthday}  Age:{int((datetime.date.today()-self.birthday).days / 365.25) }'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

