
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from companies.views import CompaniesViewSet
from transactions.views import TransactionsViewSet

router = DefaultRouter()
router.register(r'companies', CompaniesViewSet)
router.register(r'transactions', TransactionsViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
]
