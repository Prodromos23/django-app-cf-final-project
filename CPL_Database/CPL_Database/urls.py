"""
URL configuration for complianceDB project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from pep.views import remove_pep_entity_name
from .admin import combined_admin_site
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from conflict_of_interests.admin import conflict_admin_site
from .views import shutdown_view,edit_pep_info,register,pep_info_create_page,success_view,coi_info_create_page,edit_coi_info,custom_login_view


# Define router
router = DefaultRouter()

urlpatterns = [
    path('', include('CPL_Database.welcome.urls')),  # Welcome page
    path('admin/', combined_admin_site.urls),  # Combined admin interface
    path('admin/conflict_of_interests/', conflict_admin_site.urls),
    path('pep/', include('pep.urls')),  # PEP app URLs
    path('auth/', include('django.contrib.auth.urls')),  # Authentication URLs
    path('admin/api/pep_entities_names/<int:pk>/remove/', remove_pep_entity_name, name='remove_pep_entity_name'),  # API endpoint

    # below works
    # path('login/', auth_views.LoginView.as_view(), name='login'),

    # below check
    path('login/', custom_login_view.as_view(), name='login'),

    # path('login/', custom_login_view.as_view(), name='login'),

    path('admin/login/', custom_login_view.as_view(), name='admin_login'),



    # Register page
    path('register/', register, name='register'),

    path('pep_info/edit/<int:pep_info_id>/', edit_pep_info, name='edit_pep_info'),
    path('create_pep_info/', pep_info_create_page, name='create_pep_info'),
    

    path('create_coi_info/', coi_info_create_page, name='create_coi_info'),
    path('coi_info/edit/<int:coi_info_id>/', edit_coi_info, name='edit_coi_info'),

    path('success/', success_view, name='success_url'),
    path('register/', register, name='register'),
    path('registration_success/', TemplateView.as_view(template_name='registration/success.html'), name='registration_success'),
    path('shutdown/', shutdown_view, name='shutdown'),
    # path('', include(router.urls)),  # Uncomment if you need to include router URLs
]

# ________________________________




