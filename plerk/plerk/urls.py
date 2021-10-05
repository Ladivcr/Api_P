
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from companies.views import CompaniesViewSet
from transactions.views import TransactionsViewSet

#from post import views as WholeData

from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()
router.register(r'companies', CompaniesViewSet)
router.register(r'transactions', TransactionsViewSet)
#router.register(r'api', WholeData.ShowData.as_view())

urlpatterns = router.urls

urlpatterns += [
    path('admin/', admin.site.urls),
    path('api/', include('post.urls'))
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
