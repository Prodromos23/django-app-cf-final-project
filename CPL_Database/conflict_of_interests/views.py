from django.shortcuts import render
from .models import COI_Cases,COI_Cases_Subfund,COI_Dates
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.shortcuts import render,redirect
from django.http import JsonResponse
# Create your views here.




@csrf_exempt
def remove_coi_case(request, pk):
    try:
        coi_case = COI_Cases.objects.get(pk=pk)
        coi_case.removed = True
        coi_case.save()

        # Update the removal date in COI_Dates
        coi_dates = COI_Dates.objects.filter(cases_id_fk=coi_case)
        print(f"COI Dates: {coi_dates}")  # Debugging output
        if coi_dates.exists():
            coi_dates.update(date_removal=timezone.now())
        else:
            return JsonResponse({'status': 'error', 'message': 'No associated dates found'}, status=404)

        return JsonResponse({'status': 'success'})
    except COI_Cases.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Case not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)