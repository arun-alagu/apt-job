from django.urls import path, include

from rest_framework.routers import DefaultRouter

from job_seeker import views

router = DefaultRouter()
router.register('educations',views.EducationDetailViewSet)

app_name ='my'

urlpatterns =[
    path('',include(router.urls))
]