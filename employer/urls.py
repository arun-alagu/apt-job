from django.urls import path, include

from rest_framework.routers import DefaultRouter

from employer import views

router = DefaultRouter()

router.register('business-stream', views.BusinessStreamViewSet)
router.register('company-location', views.CompanyLocationViewSet)
router.register('company-profile', views.CompanyProfileViewSet)
router.register('jobs', views.JobsViewSet)
# router.register('job-list', views.JobList)

app_name = 'employer'

urlpatterns = [
    path('', include(router.urls)),
    # path('job-list', views.JobList.as_view()),
    path('job-list', views.JobList),
    path('job-list/<int:pk>', views.JobDetails.as_view()),
    path('job-create/', views.ListCreateJobPostView.as_view()),
    path('job-edit/<int:pk>', views.ManageJobPostView.as_view()),
    # path("create-business-stream/", views.BusinessStreamCreateList.as_view()),
    # path("profile/", views.userProfileDetail.as_view())
]
