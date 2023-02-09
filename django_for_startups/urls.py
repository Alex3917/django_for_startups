# Standard Library imports

# Core Django imports
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

# Third-party imports
from rest_framework_simplejwt.views import TokenRefreshView

# App imports
from app.views import account_management_views


urlpatterns = [
    path("admin/", admin.site.urls),

    path('api-token-auth/', account_management_views.CustomTokenObtainPairView.as_view()),
    path('api-token-refresh/', TokenRefreshView.as_view()),
    
    path("account_management/user", account_management_views.User.as_view(),),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
