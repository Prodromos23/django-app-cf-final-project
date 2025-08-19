from django.urls import path
from . import views
from .admin import conflict_admin_site
from .views import remove_coi_case,create_coi_info

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/conflict_of_interests/', conflict_admin_site.urls),
    path('admin/api/coi_cases/<int:pk>/remove/', remove_coi_case, name='remove_coi_case'),
    # path('create-coi-info/', create_coi_info, name='create_coi_info'),
    # Add other URL patterns for the conflicts_of_interest app
]