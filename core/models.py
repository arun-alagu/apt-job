from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


class UserManager(BaseUserManager):

    def create_user(self, email, name, password=None, **extra_fields):
        """Creates and saves new user"""

        if not email:
            raise ValueError('Users must have an email address')
        if not name:
            raise ValueError('Users must have a name')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.name = name
        user.save(using=self._db)

        return user

    def create_staffuser(self, email, password, name):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            name,
            password=password
        )
        user.is_staff = True
        user.save(using=self._db)

        return user

    def create_superuser(self,  name, email, password):
        """Creates a new superuser"""

        user = self.create_user(email, name, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model support using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

# class Tag(models.Model):
#     """Tag to be used for a job"""

#     name = models.CharField(max_length=255)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )

#     def __str__(self):
#         return self.name


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
        choices=GENDER_CHOICES,
    )
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    phone_number = models.PositiveBigIntegerField(unique=True)
    disabled = models.BooleanField(default=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'is_staff': False},
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
        limit_choices_to={'is_staff': False},
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.certified_degree_name


class ExperienceDetail(models.Model):
    """Job seekers experience information"""

    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    company_name = models.CharField(max_length=255)
    job_location_city = models.CharField(max_length=50)
    job_location_state = models.CharField(max_length=50)
    job_location_country = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={
                             'is_staff': False}, on_delete=models.CASCADE)

    def __str__(self):
        return self.job_title


class SkillSet(models.Model):
    """Skill set Database"""

    skill_set_name = models.CharField(max_length=50)

    def __str__(self):
        return self.skill_set_name


class SeekerSkillSet(models.Model):
    """Skills accquired by the applicant"""

    skills = ArrayField(models.CharField(max_length=50))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={
                             'is_staff': False}, on_delete=models.CASCADE)


class CompanyProfile(models.Model):
    """company profile"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, limit_choices_to={
        'is_staff': True}, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=100)
    profile_description = models.TextField()
    business_stream = models.CharField(max_length=255)
    established_date = models.DateTimeField()
    company_url = models.URLField()


class CompanyLocation(models.Model):
    """Job Location to be used for job post"""

    street_address = models.TextField()
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    pincode = models.CharField(max_length=50)
    user = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)


class BusinessStream(models.Model):
    """Business Stream dataset database"""

    business_stream_name = models.CharField(max_length=50)
    user = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)


class JobPost(models.Model):
    """Job post seen by all users"""

    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    roles_responsibilities = models.TextField()
    education = ArrayField(models.CharField(max_length=255))
    industry_type = models.CharField(max_length=255)
    job_location = ArrayField(models.CharField(max_length=50))
    employment_type = ArrayField(models.CharField(max_length=50))
    min_experience = models.PositiveIntegerField()
    min_salary = models.PositiveIntegerField()
    max_salary = models.PositiveIntegerField()
    skills = ArrayField(models.CharField(max_length=50))
    openings = models.PositiveIntegerField()
    created_date = models.DateTimeField(auto_now_add=True)
    company_name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        limit_choices_to={
            'is_staff': True},
        on_delete=models.CASCADE
    )


class JobPostActivity(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={
                             'is_staff': False}, on_delete=models.CASCADE)
    job_post = models.ForeignKey(
        JobPost, on_delete=models.CASCADE)
    apply_date = models.DateTimeField(auto_now_add=True)
