from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.utils import timezone


class UserManager(BaseUserManager):
    # Creates and saves User with the given email and password
    def create_user(self, email, password=None, first_name=None, last_name=None):
        if not email:
            raise ValueError('Enter an email adress')
        if not first_name:
            raise ValueError('Enter a first name')
        if not last_name:
            raise ValueError('Enter a last name')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    # Creates and saves a superuser with the give email and password
    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email, password=password,
                                first_name=first_name, last_name=last_name)
        user.staff = True
        user.role = 1
        user.save(using=self.db)
        return user


# Model for custom User
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address', max_length=200, unique=True)
    first_name = models.CharField(
        verbose_name='first name', max_length=200)
    last_name = models.CharField(
        verbose_name="last name", max_length=200)
    ROLE_CHOICES = (
        (1, 'administrator'),
        (2, 'pracownik dziekanatu'),
        (3, 'promotor'),
        (4, 'student'),
    )
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, default=4)
    date_joined = models.DateTimeField(
        verbose_name='date joined', default=timezone.now)
    last_login = models.DateTimeField(
        verbose_name='last login', default=timezone.now)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'last_name')

    class Meta:
        db_table = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return '%s %s %s %s' % (self.email, self.first_name, self.last_name, self.role)

    # For checking permissions. Every admin have all permissions.
    def has_perm(self, perm, obj=None):
        return self.role

    # Does the user have permissions to view the app?
    def has_module_perms(self, app_label):
        return self.role

    # What is the user role?
    @property
    def which_role(self):
        return self.role

    # When user joined?
    @property
    def when_joined(self):
        return self.date_joined

    # When user logged last time?
    @property
    def when_last_login(self):
        return self.last_login

    # Is the user active?
    @property
    def is_active(self):
        return self.active

    # Is the user a member of staff?
    @property
    def is_staff(self):
        return self.staff
