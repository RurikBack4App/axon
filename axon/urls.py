from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from users.views import UserViewSet
from .views import redirect_to_swagger

schema_view = get_schema_view(
    openapi.Info(
        title="Axon Loan Management API",
        default_version='v1',
        description="Streamline your loan origination, review, and tracking processes.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="preciousimoniakemu@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True, 
    permission_classes=(permissions.AllowAny,), 
)

urlpatterns = [
    path('', redirect_to_swagger), # Redirect root URL 
    
    # Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('auth/register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain'),  # JWT Login
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # JWT Refresh
    
    # Swagger documentation URLs
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # Other apps urls
    path('api/', include('loans.urls')),
    path('api/users/', include('users.urls')),
]
