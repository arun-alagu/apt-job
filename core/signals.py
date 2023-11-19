from core.models import SeekerProfile, EducationDetail

from django.db.models.signals import pre_save, post_save

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.dispatch import receiver


class SeekerProfileSignal:
    def check_gender(sender, instance, *args, **kwargs):
        if instance.gender is None:
            raise ValueError('Gender is needed')
        elif not (instance.gender == 'M' or instance.gender == 'F' or instance.gender == 'O'):
            raise ValueError('Select a valid gender')
        pass

    pre_save.connect(check_gender, sender=SeekerProfile)


class EducationDetailSignal:
    def check_year(sender, instance, *args, **kwargs):
        if instance.start_year >= instance.complete_year:
            raise ValueError('Started year must be less than Completed year')

    pre_save.connect(check_year, sender=EducationDetail)


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_profile(sender, instance, created, **kwargs):
#     try:
#         if created:
#             # print("Created profile")
#             SeekerProfile.objects.create(user=instance).save()
#     except Exception as err:
#         print(f'Error creating user profile!\n{err}')
