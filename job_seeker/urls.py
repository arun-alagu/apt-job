from django.urls import path, include

from rest_framework.routers import DefaultRouter

from job_seeker import views

router = DefaultRouter()
# router.register('profile', views.UserProfileViewSet)
# router.register('educations', views.EducationDetailView,
#                 basename="seeker-educations")

app_name = 'job_seeker'

urlpatterns = [
    # path('', include(router.urls)),
    path("profiles/", views.ListCreateUserProfileView.as_view(),
         name="create-get-seeker-profile"),
    path("profiles/<int:pk>", views.ManageUserProfileView.as_view(),
         name="edit-seeker-profile"),
    path("profile-view/", views.RetrieveUserProfileView.as_view()),
    path("educations/", views.ListCreateEducationDetailView.as_view(),
         name="create-get-seeker-educations"),
    path("educations/<int:pk>", views.ManageEducationDetailView.as_view(),
         name="edit-seeker-education"),
    path("experiences/", views.ListCreateExperienceDetailView.as_view(),
         name="create-get-seeker-experiences"),
    path("experiences/<int:pk>", views.ManageExperienceDetailView.as_view(),
         name="edit-seeker-experiences"),
    path("skills/", views.ListCreateSeekerSkillSetView.as_view(),
         name="create-get-seeker-skills"),
    path("skills/<int:pk>", views.ManageSeekerSkillSetView.as_view(),
         name="edit-seeker-skill"),
    path("applied-jobs/", views.AppliedJobsList.as_view()),
]
