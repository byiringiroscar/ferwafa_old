from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, email, full_name, phone_number, password=None):
        if not email:
            raise ValueError("user must have an email address")
        if not full_name:
            raise ValueError("user must have full_name")
        if not phone_number:
            raise ValueError("Instructor must have phone_number")
        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, full_name, phone_number, password):
        if not email:
            raise ValueError("user must have an email address")
        if not full_name:
            raise ValueError("user must have full_name")
        if not phone_number:
            raise ValueError("Instructor must have phone_number")
        user = self.create_user(
            email,
            full_name=full_name,
            phone_number=phone_number,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name, phone_number, password):

        user = self.create_user(
            email,
            full_name=full_name,
            phone_number=phone_number,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    full_name = models.CharField(max_length=255)
    phone_number = PhoneNumberField(blank=False)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user; non super-user
    admin = models.BooleanField(default=False)  # a superuser
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name', 'phone_number']  # Email & Password are required by default.
    objects = UserManager()

    def get_full_name(self):
        return f'{self.full_name}--{self.email}'

    def get_short_name(self):
        return self.full_name

    def __str__(self):
        return f'{self.full_name}--{self.email}'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin


class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='images/', default='profile.png')
    user_location = models.CharField(max_length=100, blank=True, null=True)
    user_roles = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f'{self.user.full_name}'

    class Meta:
        verbose_name_plural = "User_profile"
        ordering = ['-id']
