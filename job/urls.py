from django.urls import path, include
from rest_framework.routers import DefaultRouter

from job import views


router = DefaultRouter()
# router.register('tags', views.TagViewSet)
# router.register('ingredients', views.IngredientViewSet)
# router.register('jobs', views.JobViewSet)

app_name = 'job'

urlpatterns = [
    # path('job', include(router.urls)),
    path('jobs/', views.getJobs, name="jobs"),
    path('jobs/<int:pk>', views.getJob, name="job"),
    path('skills/', views.SkillsList.as_view(), name="skills"),
    path('job-list', views.JobList.as_view()),
    path('recommended-jobs/<int:pk>',
         views.getRecommendedJob, name="recommended-jobs"),
    path('applied-users', views.ListJobPostActivity.as_view(), name="applied-users"),
    path("job-post-activities/", views.ListCreateJobPostActivityView.as_view()),
    path("job-post-activities/<int:pk>",
         views.RetrieveDestroyJobPostActivityView.as_view()),
    # path('skills/<int:pk>', views.getJob, name="skill")
]
