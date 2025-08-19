import openpyxl
from django.http import HttpResponse
from pep.models import PEP_Info,PEP_Dates,PEP_Entities_Subfund
# from .models import PEP_Info, PEP_Entities_Names, PEP_Names, Person_Reviewers
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


# @admin.action(description='Mark selected entities as removed')
def mark_as_removed(modeladmin, request, queryset):
    for entity in queryset:
        entity.removed = True
        entity.save()
        # Update the removal date in PEP_Dates
        pep_dates = PEP_Dates.objects.filter(entities_names_id_fk=entity)
        if pep_dates.exists():
            for pep_date in pep_dates:
                pep_date.date_removal = timezone.now()
                pep_date.save()
        else:
            modeladmin.message_user(request, f'No associated dates found for {entity}', level='error')

mark_as_removed.short_description = 'Mark selected entities as removed'


def export_to_excel(modeladmin, request, queryset):
    # Create an in-memory workbook
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Exported Data'

    # Define the column headers
    columns = ['Entity Name', 'PEP Name', 'Date Added', 'Date Validation RC', 'Date Approval MC', 'Date Approval BRD', 'Date Removal', 'Date Updated Last']
    worksheet.append(columns)

    # Add data to the worksheet
    for obj in queryset:
        row = [
            obj.entities_names_id_fk.entities_id_fk.entity_name,
            obj.entities_names_id_fk.names_id_fk.pep_name,
            obj.date_added,
            obj.date_validation_rc,
            obj.date_approval_mc,
            obj.date_approval_brd,
            obj.date_removal,
            obj.date_updated_last
        ]
        worksheet.append(row)

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=exported_data.xlsx'
    workbook.save(response)
    return response

export_to_excel.short_description = 'Export selected to Excel'


def export_info_to_excel(modeladmin, request, queryset):
    # Create an in-memory workbook
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Exported Data'

    # Define the column headers
    columns = [
        'PEP Info ID', 'Entity Name', 'PEP Name', 'Reviewer Name', 'RC Validator Name',
        'Slamlux Classification', 'TA Classification', 'Slamlux Estimation', 'TA Estimation',
        'Nationality', 'Position', 'Date Added', 'Date RC Validation','Date Approval MC', 'Date Approval Board', 'Date Updated',
        'Comment Screening', 'Comment Assessment', 'Comment MC Board', 'PEP Remove Reason', 'Fund Name', 'Subfund Name','Removed'
    ]
    worksheet.append(columns)

    # Custom query to join data from PEP_Info and related tables
    data = PEP_Info.objects.select_related(
        'entities_names_id_fk__entities_id_fk',
        'entities_names_id_fk__names_id_fk',
        'person_reviewers_id_fk',
        'rc_validation_id_fk',
        'slamlux_classification_id_fk',
        'ta_classification_id_fk',
        'slamlux_estimation_id_fk',
        'ta_estimation_id_fk',
        'pep_nationality_id_fk',
        'pep_dates_id_fk'
    ).prefetch_related('entities_names_id_fk__entities_id_fk__pep_entities_subfund_set__subfund_id_fk__fund_id_fk').all()

    # Debugging output
    print(f"Retrieved {data.count()} records")
    print(data)

    # Add data to the worksheet
    for obj in data:
        print(f"PEP_Info ID: {obj.pep_info_id}, Entity Name: {obj.entities_names_id_fk.entities_id_fk.entity_name}, PEP Name: {obj.entities_names_id_fk.names_id_fk.pep_name}, Reviewer: {obj.person_reviewers_id_fk.lastname}")
        entity = obj.entities_names_id_fk.entities_id_fk
        subfunds = entity.pep_entities_subfund_set.all()
        # subfunds = PEP_Entities_Subfund.objects.filter(entities_id_fk=entity)
        print(f"Subfunds: {subfunds}")
        for subfund in subfunds:
            print(subfund)
            dates = PEP_Dates.objects.filter(entities_names_id_fk = obj.entities_names_id_fk)
            for date in dates:
                print(obj.pep_info_id)
                row = [
                    obj.pep_info_id,
                    obj.entities_names_id_fk.entities_id_fk.entity_name,
                    obj.entities_names_id_fk.names_id_fk.pep_name,
                    f"{obj.person_reviewers_id_fk.lastname} {obj.person_reviewers_id_fk.firstname}" if obj.person_reviewers_id_fk else '',
                    f"{obj.rc_validation_id_fk.lastname} {obj.rc_validation_id_fk.firstname}" if obj.rc_validation_id_fk else '',
                    obj.slamlux_classification_id_fk.classification_status if obj.slamlux_classification_id_fk else '',
                    obj.ta_classification_id_fk.classification_status if obj.ta_classification_id_fk else '',
                    obj.slamlux_estimation_id_fk.estimation_status if obj.slamlux_estimation_id_fk else '',
                    obj.ta_estimation_id_fk.estimation_status if obj.ta_estimation_id_fk else '',
                    obj.pep_nationality_id_fk.nationality if obj.pep_nationality_id_fk else '',
                    obj.entities_names_id_fk.names_id_fk.position,
                    date.date_added,
                    date.date_validation_rc,
                    date.date_approval_mc,
                    date.date_approval_brd,
                    date.date_updated_last,
                    obj.comment_screening,
                    obj.comment_assessment,
                    obj.comment_mc_board,
                    obj.pep_remove_reason,
                    subfund.subfund_id_fk.fund_id_fk.fund_name if subfund.subfund_id_fk.fund_id_fk else '',
                    subfund.subfund_id_fk.subfund_name if subfund.subfund_id_fk else '',
                    obj.entities_names_id_fk.removed
                ]
                worksheet.append(row)
                print(f"Added row: {row}")

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=pep_info.xlsx'
    # Add autofilter to the first row
    worksheet.auto_filter.ref = worksheet.dimensions
    workbook.save(response)
    return response

export_info_to_excel.short_description = 'Export PEP Info to Excel'



# def mark_as_updated(modeladmin, request, queryset):
#     for entity in queryset:
#         entity.save()  # Save the entity to trigger any updates
#         # Update the date_updated_last in PEP_Dates
#         pep_dates = PEP_Dates.objects.get(entities_names_id_fk=entity.entities_names_id_fk)
#         pep_dates.date_updated_last = timezone.now().date()
#         pep_dates.save()
