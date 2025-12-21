from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),

    # Django auth (login/logout)
    path("accounts/", include("django.contrib.auth.urls")),

    # CRM
    path("", include(("crm.urls", "crm"), namespace="crm")),
]
