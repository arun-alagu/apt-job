from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves new user"""

        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email= self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, password):
        """Creates a new superuser"""

        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

class Tag(models.Model):
    """Tag to be used for a job"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name

class SeekerProfile(models.Model):
    """Seeker profile for job seekers"""

    MALE = 'M'
    FEMALE = 'F'
    OTHERS = 'O'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHERS, 'Others'),
    ]
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES
        )
    address = models.TextField()
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50, null=False, blank=False, unique=True)
    disabled = models.BooleanField(default=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )

    def __str__(self):
        return self.first_name+" "+self.last_name


class EducationDetail(models.Model):
    """Job seekers education information"""

    certified_degree_name = models.CharField(max_length=50)
    major = models.CharField(max_length=50)
    institute_university_name = models.CharField(max_length=50)
    start_year = models.PositiveIntegerField()
    complete_year = models.PositiveIntegerField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    cgpa = models.DecimalField(max_digits=4, decimal_places=2)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    
    def __str__(self):
        return self.certified_degree_name


# class JobLocation(models.Model):
#     """Job Location to be used for job post"""

#     street_address = models.TextField()
#     city = models.CharField(max_length=255)
#     state = models.CharField(max_length=255)
#     country = models.CharField(max_length=255)
#     zip = models.CharField(max_length=50)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete = models.CASCADE
#     )
