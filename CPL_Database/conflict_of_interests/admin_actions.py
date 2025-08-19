import openpyxl
from django.http import HttpResponse
from .models import COI_Info,COI_Dates,COI_Cases_Subfund
import logging
from django.utils import timezone

logger = logging.getLogger(__name__)


# @admin.action(description='Mark selected entities as removed')
def mark_as_removed(modeladmin, request, queryset):
    for case in queryset:
        case.removed = True
        case.save()
        # Update the removal date in PEP_Dates
        coi_dates = COI_Dates.objects.get(cases_id_fk=case)
        coi_dates.date_removal = timezone.now()
        coi_dates.save()

mark_as_removed.short_description = 'Mark selected entities as removed'


def export_to_excel(modeladmin, request, queryset):
    # Create an in-memory workbook
    workbook = openpyxl.Workbook()
    worksheet = workbook.active
    worksheet.title = 'Exported Data'

    # Define the column headers
    columns = ['Area of Conflict', 'Date Added', 'Event Description' ,'Date Validation RC', 'Date Approval MC', 'Date Approval BRD', 'Date Removal', 'Date Updated Last']
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
    columns = ['COI Info ID','Area of Conflict', 'Date Added', 'Event Description', 'Subfund', 'Fund', 'isProven', 'Unit', 'Management of Conflict/ Mitigation Measures', 'isInvestor Informed', 'Status', 'Date MC Review','Date Board Review','Date Last Updated', 'Removed']
    worksheet.append(columns)
    # Custom query to join data from PEP_Info and related tables
    data = COI_Info.objects.select_related(
        'cases_id_fk',
        'coi_dates_id_fk',
        'status_id_fk'
    ).prefetch_related('cases_id_fk__coi_cases_subfund_set__subfund_id_fk__fund_id_fk').all()

    # Debugging output
    print(f"Retrieved {data.count()} records")
    print(data)

    # Add data to the worksheet
    for obj in data:
        # print(f"PEP_Info ID: {obj.pep_info_id}, Entity Name: {obj.entities_names_id_fk.entities_id_fk.entity_name}, PEP Name: {obj.entities_names_id_fk.names_id_fk.pep_name}, Reviewer: {obj.person_reviewers_id_fk.lastname}")
        case = obj.cases_id_fk
        subfunds = case.coi_cases_subfund_set.all()
        # subfunds = PEP_Entities_Subfund.objects.filter(entities_id_fk=entity)
        print(f"Subfunds: {subfunds}")

        for subfund in subfunds:
            print(subfund)
            dates = COI_Dates.objects.filter(cases_id_fk = obj.cases_id_fk)
            for date in dates:
                row = [
                    obj.coi_info_id,
                    obj.cases_id_fk.area_of_conflict,
                    date.date_added,
                    obj.cases_id_fk.event_description,
                    subfund.subfund_id_fk.subfund_name if subfund.subfund_id_fk else '',
                    subfund.subfund_id_fk.fund_id_fk.fund_name if subfund.subfund_id_fk.fund_id_fk else '',
                    obj.isProven,
                    obj.unit,
                    obj.mitigation_measures,
                    obj.isInvestorInformed,
                    obj.status_id_fk.status_description,
                    date.date_review_mc,
                    date.date_review_brd,
                    # f"{obj.person_reviewers_id_fk.lastname} {obj.person_reviewers_id_fk.firstname}" if obj.person_reviewers_id_fk else '',
                    # f"{obj.rc_validation_id_fk.lastname} {obj.rc_validation_id_fk.firstname}" if obj.rc_validation_id_fk else '',
                    date.date_updated_last,
                    obj.cases_id_fk.removed
                ]
                worksheet.append(row)
                print(f"Added row: {row}")

    # Create an HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=coi_info.xlsx'
    # Add autofilter to the first row
    worksheet.auto_filter.ref = worksheet.dimensions
    workbook.save(response)
    return response

export_info_to_excel.short_description = 'Export COI Info to Excel'



# def mark_as_updated(modeladmin, request, queryset):
#     for entity in queryset:
#         entity.save()  # Save the entity to trigger any updates
#         # Update the date_updated_last in PEP_Dates
#         pep_dates = PEP_Dates.objects.get(entities_names_id_fk=entity.entities_names_id_fk)
#         pep_dates.date_updated_last = timezone.now().date()
#         pep_dates.save()
