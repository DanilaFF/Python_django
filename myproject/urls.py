from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Админка
    path("admin/", admin.site.urls),

    # 🔐 АУТЕНТИФИКАЦИЯ (login / logout)
    path("accounts/", include("django.contrib.auth.urls")),

    # CRM
    path("", include(("crm.urls", "crm"), namespace="crm")),
]
