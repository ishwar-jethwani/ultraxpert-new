"""ultraxpert URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .sitemaps import StaticViewSitemap
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from useraccounts.views import *
from dj_rest_auth.views import PasswordChangeView, LogoutView

admin.site.site_header = settings.ADMIN_SITE_HEADER

schema_view = get_schema_view(
   openapi.Info(
      title="UltraXpert API",
      default_version='Beta',
      description="This Application Contains Expert API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

# swagger URLS
urlpatterns = [
    path("home/", home, name="home"),
    path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("admin/", admin.site.urls),
    path("file_upload/", FileUploadView.as_view(), name="file_upload"),
]

# Authentication URLS
urlpatterns += [
    path("register/", include('dj_rest_auth.registration.urls'), name="register"), 
    path("login/", LoginView.as_view(), name="login"), 
    path("logout/", LogoutView.as_view(), name="logout"), 
    path("change/", PasswordChangeView.as_view(), name="change_password"), 
    path("reset/", ResetPassword.as_view(), name="reset_password"), 
    path("verify/", VerificationView.as_view(), name="Verification"),
]

# Apps URL 
urlpatterns += [
    path("experts/", include("experts.urls")),
    path("customers/", include("customers.urls")),
    path("blogs/", include("blogs.urls")),
    path("booking/", include("booking.urls")),
    path("meetings/", include("meetings.urls")),
    path("apis/", include("apis.urls")),
    path("inspections/", include("inspections.urls")),
    path("wallet/", include("wallet.urls")),
    path("chat/", include("chat.urls")),
    path("payments/", include("payments.urls")),
    path("enterprises/", include("enterprises.urls")),
]

sitemaps = {
    'static': StaticViewSitemap,
}
#sitemap
urlpatterns += [
   path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='sitemap')
]
