from django.contrib import admin
# from CPL_Database.admin import combined_admin_site
from .models import COI_Dates,COI_Cases,COI_Cases_Subfund,COI_Info,COI_Status
from .forms import COIInfoAdminForm
from .admin_actions import export_info_to_excel,mark_as_removed
# Register your models here.

# combined_admin_site.register(COI_TypeOfConflict)
# combined_admin_site.register(COI_Dates)

class COI_Cases_SubfundInline(admin.TabularInline):
    model = COI_Cases_Subfund
    extra = 1

# @admin.register(COI_Cases)
# class COICasesAdmin(admin.ModelAdmin):
#     change_list_template = 'admin/coi_cases_change_list.html'
#     list_display = ('area_of_conflict',)
#     search_fields = ('area_of_conflict',)
#     inlines = [COI_Cases_SubfundInline]
#     actions = [mark_as_removed]

#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         return qs.all()

@admin.register(COI_Cases)
class COICasesAdmin(admin.ModelAdmin):
    change_list_template = 'admin/coi_cases_change_list.html'
    list_display = ('area_of_conflict', 'removed')
    search_fields = ('area_of_conflict',)
    actions = [mark_as_removed]
    inlines = [COI_Cases_SubfundInline]
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.all()


class ConflictAdminSite(admin.AdminSite):
    site_header = 'Conflict of Interests Administration'
    site_title = 'Conflict Admin'
    index_title = 'Conflict of Interests Site Administration'

conflict_admin_site = ConflictAdminSite(name='conflict_admin')

class ConflictOfInterestsAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        perms = super().get_model_perms(request)
        perms['change'] = True  # Ensure the section is visible
        return perms

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['title'] = 'Conflict Of Interests'
        return super().changelist_view(request, extra_context=extra_context)

# @admin.register(COI_Dates)
# class COIDatesAdmin(admin.ModelAdmin):
#     list_display = ('cases_id_fk', 'date_added', 'date_review_mc', 'date_review_brd', 'date_removal', 'date_updated_last')

#     search_fields = ('cases_id_fk__area_of_conflict', 'entities_names_id_fk__names_id_fk__pep_name')

#     list_filter = ('cases_id_fk',)

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "cases_id_fk":
#             kwargs["queryset"] = COI_Cases.objects.select_related('coi_cases_id').all()
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(COI_Dates)
class COIDatesAdmin(admin.ModelAdmin):
    list_display = ('cases_id_fk', 'date_added', 'date_review_mc', 'date_review_brd', 'date_removal', 'date_updated_last')
    search_fields = ('cases_id_fk__area_of_conflict', 'entities_names_id_fk__names_id_fk__pep_name')
    list_filter = ('cases_id_fk',)
    # actions = [export_to_excel]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "cases_id_fk":
            kwargs["queryset"] = COI_Cases.objects.select_related('coi_cases_id').all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


# @admin.register(COI_Info)
# class COIInfoAdmin(admin.ModelAdmin):
#     form = COIInfoAdminForm
#     list_display = ('coi_info_id', 'cases_id_fk', 'status_id_fk')
#     search_fields = ('cases_id_fk__area_of_conflict', 'coi_dates_id_fk'
#                     #  'pep_names_screening_id_fk__pep_name'
#                     )
#     actions = [export_info_to_excel]


@admin.register(COI_Info)
class COIInfoAdmin(admin.ModelAdmin):
    form = COIInfoAdminForm
    # list_display = ('coi_info_id', 'cases_id_fk', 'isProven', 'unit', 'mitigation_measures', 'isInvestorInformed', 'status_id_fk', 'coi_dates_id_fk')
    list_display = ('coi_info_id', 'cases_id_fk', 'isProven', 'unit', 'mitigation_measures', 'isInvestorInformed', 'status_id_fk')
    search_fields = ('cases_id_fk__area_of_conflict', 'status_id_fk__status_description')
    actions = [export_info_to_excel]

    def delete_model(self, request, obj):
        obj.delete()

