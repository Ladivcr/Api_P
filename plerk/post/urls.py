
from django.urls import path, include

from post import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

urlpatterns = [
    path('', views.ShowData.as_view()),
    path('<str:id>', views.FilterData.as_view())
]