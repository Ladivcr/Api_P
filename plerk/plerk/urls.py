
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from companies.views import CompaniesViewSet

router = DefaultRouter()
router.register(r'companies', CompaniesViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
]
