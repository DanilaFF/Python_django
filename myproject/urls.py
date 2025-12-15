from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),

    # страницы логина/логаута
    path('login/', LoginView.as_view(template_name='crm/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    # наше приложение CRM
    path('', include('crm.urls')),
]
