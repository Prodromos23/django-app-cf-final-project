from django.contrib import admin
from django.contrib.auth.models import User, Group
from pep.models import PEP_Entities, PEP_Names, PEP_Dates, PEP_Entities_Names, PEP_Info,Fund,Subfund,PEP_Entities_Subfund,PEP_Name_Screening,PEP_Estimations,PEP_Classifications,PEP_Nationality,Person_Reviewers,ServiceProviderType
from conflict_of_interests.models import COI_Dates,COI_Cases,COI_Cases_Subfund,COI_Info,COI_Status
from pep.admin import PEPInfoAdmin,PEPEntitiesNamesAdmin,PEPDatesAdmin,SubfundAdmin,PEPNameAdmin,PEPEntitiesAdmin
from conflict_of_interests.admin import COICasesAdmin,COIInfoAdmin


MODEL_ORDER = {
    'pep': ['PEP_Entities', 'PEP_Names', 'PEP_Dates', 'PEP_Entities_Names', 'PEP_Info'],
    'conflict_of_interests': ['COI_Cases', 'COI_Dates', 'COI_Info', 'COI_Status', 'COI_Cases_Subfund'],
    # Add other apps and their model order as needed
}
APP_ORDER = ['pep', 'conflict_of_interests', 'auth']

class CombinedAdminSite(admin.AdminSite):
    site_header = 'Compliance Database Administration'
    site_title = 'Database Admin'
    index_title = 'Database Administration'

    def has_permission(self, request):
        return request.user.is_active and request.user.is_staff

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        user_groups = request.user.groups.values_list('name', flat=True)

        if 'Group1' in user_groups:
            app_list = self.show_all_models(app_list)
        elif 'Group2' in user_groups:
            app_list = self.show_specific_models(app_list, ["PEP_Entities", "PEP_Names", "PEP_Entities_Names", "PEP_Dates", "PEP_Info","COI_Cases","COI_Info","COI_Dates"])

        return self.order_models(app_list)

    def show_all_models(self, app_list):
        for app in app_list:
            print(f"App: {app['name']}, Models: {[model['object_name'] for model in app['models']]}")
        return app_list

    def show_specific_models(self, app_list, model_names):
        for app in app_list:
            app['models'] = [model for model in app['models'] if model['object_name'] in model_names]
            print(f"App: {app['name']}, Models: {[model['object_name'] for model in app['models']]}")
        return app_list

    def order_models(self, app_list):
        for app in app_list:
            if app['app_label'] in MODEL_ORDER:
                ordered_models = []
                unordered_models = {model['object_name']: model for model in app['models']}
                for model_name in MODEL_ORDER[app['app_label']]:
                    if model_name in unordered_models:
                        ordered_models.append(unordered_models.pop(model_name))
                ordered_models.extend(unordered_models.values())
                app['models'] = ordered_models
        return app_list
    
    # def order_apps(self, app_list):
    #     ordered_apps = []
    #     unordered_apps = {app['app_label']: app for app in app_list}
    #     for app_label in APP_ORDER:
    #         if app_label in unordered_apps:
    #             ordered_apps.append(unordered_apps.pop(app_label))
    #     ordered_apps.extend(unordered_apps.values())
    #     print(f"Ordered Apps: {[app['app_label'] for app in ordered_apps]}")  # Debugging output
    #     return ordered_apps

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Conflict Of Interests'
        return super().changelist_view(request, extra_context=extra_context)

combined_admin_site = CombinedAdminSite(name='combined_admin')

# Function to register models only if not already registered
def register_model(admin_site, model, model_admin=None):
    if not admin_site.is_registered(model):
        admin_site.register(model, model_admin)
        # print(f"Registered model: {model.__name__}")


# Register all models here
register_model(combined_admin_site, PEP_Entities,PEPEntitiesAdmin)
register_model(combined_admin_site, PEP_Names,PEPNameAdmin)
register_model(combined_admin_site, PEP_Dates,PEPDatesAdmin)
register_model(combined_admin_site, PEP_Entities_Names,PEPEntitiesNamesAdmin)
register_model(combined_admin_site, PEP_Info,PEPInfoAdmin)
register_model(combined_admin_site, Fund)
register_model(combined_admin_site, Subfund,SubfundAdmin)
register_model(combined_admin_site, PEP_Entities_Subfund)
register_model(combined_admin_site, PEP_Name_Screening)
register_model(combined_admin_site, PEP_Estimations)
register_model(combined_admin_site, PEP_Classifications)
register_model(combined_admin_site, PEP_Nationality)
register_model(combined_admin_site, Person_Reviewers)
register_model(combined_admin_site, ServiceProviderType)
# COI_Dates,COI_Cases,COI_Cases_Subfund,COI_Info,COI_Status
register_model(combined_admin_site, COI_Dates)
register_model(combined_admin_site, COI_Cases,COICasesAdmin)
register_model(combined_admin_site, COI_Cases)
register_model(combined_admin_site, COI_Cases_Subfund)
register_model(combined_admin_site, COI_Status)
register_model(combined_admin_site, COI_Info,COIInfoAdmin)

# Register authentication models
combined_admin_site.register(User)
combined_admin_site.register(Group)

# ___________________________________________________

