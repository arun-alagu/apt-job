from core.models import SeekerProfile, EducationDetail

from django.db.models.signals import pre_save

class SeekerProfileSignal :
    def check_gender(sender, instance, *args, **kwargs):
        if instance.gender is None:
            raise ValueError('Gender is needed')
        elif not (instance.gender == 'M' or instance.gender == 'F' or instance.gender == 'O'):
            raise ValueError('Select a valid gender')
        pass
    
    pre_save.connect(check_gender, sender=SeekerProfile)

class EducationDetailSignal :
    def check_year(sender, instance, *args, **kwargs):
        if instance.start_year >= instance.complete_year:
            raise ValueError('Started year must be less than Completed year')
    
    pre_save.connect(check_year, sender=EducationDetail)
