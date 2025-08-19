
from django.contrib import admin
from .models import Fund, Subfund, PEP_Entities, PEP_Entities_Subfund, PEP_Names, PEP_Entities_Names, PEP_Dates, PEP_Name_Screening, PEP_Classifications, PEP_Estimations, Person_Reviewers, ServiceProviderType, PEP_Info, PEP_Nationality
from pep.forms import PEPNameForm, PEPInfoAdminForm
from .admin_actions import *

class PEP_Entities_SubfundInline(admin.TabularInline):
    model = PEP_Entities_Subfund
    extra = 1

@admin.register(PEP_Entities)
class PEPEntitiesAdmin(admin.ModelAdmin):
    list_display = ('entity_name',)
    search_fields = ('entity_name',)
    inlines = [PEP_Entities_SubfundInline]


@admin.register(PEP_Names)
class PEPNameAdmin(admin.ModelAdmin):
    form = PEPNameForm

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        entities_id_fk = form.cleaned_data.get('entities_id_fk')
        if entities_id_fk:
            pep_entities_names = PEP_Entities_Names.objects.create(names_id_fk=obj, entities_id_fk=entities_id_fk)
            PEP_Dates.objects.create(entities_names_id_fk=pep_entities_names)

class SubfundAdmin(admin.ModelAdmin):
    list_display = ('subfund_name', 'fund_id_fk', 'is_subfund', 'is_umbrella')
    search_fields = ('subfund_name',)

@admin.register(PEP_Dates)
class PEPDatesAdmin(admin.ModelAdmin):
    list_display = ('entities_names_id_fk', 'date_added', 'date_validation_rc', 'date_approval_mc', 'date_approval_brd', 'date_removal', 'date_updated_last')
    search_fields = ('entities_names_id_fk__entities_id_fk__entity_name', 'entities_names_id_fk__names_id_fk__pep_name')
    list_filter = ('entities_names_id_fk',)
    actions = [export_to_excel]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "entities_names_id_fk":
            kwargs["queryset"] = PEP_Entities_Names.objects.select_related('entities_id_fk', 'names_id_fk').all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(PEP_Entities_Subfund)
class PEP_Entities_SubfundAdmin(admin.ModelAdmin):
    list_display = ('entities_id_fk', 'subfund_id_fk')
    search_fields = ('entities_id_fk__entity_name', 'subfund_id_fk__subfund_name')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('entities_id_fk', 'subfund_id_fk')


@admin.register(PEP_Entities_Names)
class PEPEntitiesNamesAdmin(admin.ModelAdmin):
    change_list_template = 'admin/pep_entities_names_change_list.html'
    list_display = ('entities_id_fk', 'names_id_fk', 'removed')
    search_fields = ('entities_id_fk__entity_name', 'names_id_fk__pep_name')
    actions = [mark_as_removed]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.all()

    def delete_model(self, request, obj):
        PEP_Info.objects.filter(entities_names_id_fk=obj).delete()
        PEP_Dates.objects.filter(entities_names_id_fk=obj).delete()
        super().delete_model(request, obj)

@admin.register(PEP_Info)
class PEPInfoAdmin(admin.ModelAdmin):
    form = PEPInfoAdminForm
    list_display = ('pep_info_id', 'entities_names_id_fk', 'pep_names_screening_id_fk', 'person_reviewers_id_fk', 'rc_validation_id_fk', 'pep_nationality_id_fk', 'is_rr_validated')

    search_fields = ('entities_names_id_fk__entities_id_fk__entity_name', 'pep_names_screening_id_fk__pep_name', 'person_reviewers_id_fk__reviewer_name', 'rc_validation_id_fk__reviewer_name', 'pep_nationality_id_fk')
    actions = [export_info_to_excel]

    # def delete_model(self, request, obj):
    #     # Ensure related PEP_Dates instances are deleted
    #     PEP_Dates.objects.filter(entities_names_id_fk=obj.entities_names_id_fk).delete()
    #     # Ensure related PEP_Entities_Names instances are deleted
    #     PEP_Entities_Names.objects.filter(entities_id_fk=obj.entities_names_id_fk.entities_id_fk, names_id_fk=obj.entities_names_id_fk.names_id_fk).delete()
    #     # Ensure related PEP_Entities_Subfund instances are deleted
    #     PEP_Entities_Subfund.objects.filter(entities_id_fk=obj.entities_names_id_fk.entities_id_fk).delete()
    #     super().delete_model(request, obj)

    def delete_model(self, request, obj):
        obj.delete()