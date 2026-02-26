from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
import random
# Create your models here.
class device_logs(models.Model):
    current_device = models.IntegerField(blank=True, null=True)
    current_packet_number = models.IntegerField(blank=True, null=True)
    device_id = models.CharField(max_length=50, blank=True, null=True)
    pckt_id = models.CharField(max_length=50, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    pckt_no = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(default=now, blank=True, null=True)
    actual_date_time = models.CharField(max_length=500, blank=True, null=True)
    is_sound_play = models.IntegerField()
    class Meta:
        verbose_name = "device_logs"
        db_table = "device_logs"


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class user(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=599, null=True, default=None)
    mobile = models.CharField(max_length=50)
    image = models.ImageField(upload_to='user')
    created_at = models.DateTimeField(default=now, blank=True, null=True)
    updated_at = models.DateTimeField(default=now, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set_permissions', blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile', 'gender', 'dob', 'address', 'website', 'brief']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def save(self, *args, **kwargs):
        if self.image:
            filename = self.image.name.split('/')[-1]
            self.image.name = filename
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "User"
        db_table = "users"




def generate_random_color():
    """Generate a random hex color code."""
    return '#{:06x}'.format(random.randint(0, 0xFFFFFF))

class deviceconfig(models.Model):
    device_id = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=False)
    color = models.CharField(
        max_length=7,
        default=generate_random_color,  # Use the function without calling it
        unique=True  # Ensures uniqueness in the database
    )
    created_at = models.DateTimeField(default=now, blank=True, null=True)
    updated_at = models.DateTimeField(default=now, blank=True, null=True)

    class Meta:
        verbose_name = "device_config"
        db_table = "device_config"