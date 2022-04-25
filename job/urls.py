from django.urls import path, include
from rest_framework.routers import DefaultRouter

from job import views


router = DefaultRouter()
router.register('tags', views.TagViewSet)
# router.register('ingredients', views.IngredientViewSet)
# router.register('jobs', views.JobViewSet)

app_name = 'job'

urlpatterns = [
    path('', include(router.urls))
]