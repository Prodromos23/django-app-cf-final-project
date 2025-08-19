from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from pep.models import PEP_Names,PEP_Entities_Names,Subfund,PEP_Entities_Subfund, PEP_Entities,PEP_Dates
from pep.serializers import PEPNameSerializer,EntitiesSerializer
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone


# def change_title(request):
#     return render(request,'api.html')

class PEPNameViewSet(viewsets.ModelViewSet):
    queryset = PEP_Names.objects.all()
    serializer_class = PEPNameSerializer

    def perform_create(self, serializer):
        pep_name = serializer.save()
        # Create the relationship in PEP_Entities_Names table
        PEP_Entities_Names.objects.create(names_id_fk=pep_name, entities_id_fk=pep_name.entities_id_fk)


@csrf_exempt
def remove_pep_entity_name(request, pk):
    try:
        pep_entity_name = PEP_Entities_Names.objects.get(pk=pk)
        pep_entity_name.removed = True
        pep_entity_name.save()

        # Update the removal date in PEP_Dates
        pep_dates = PEP_Dates.objects.filter(entities_names_id_fk=pep_entity_name)
        if pep_dates.exists():
            pep_dates.update(date_removal=timezone.now())
        else:
            return JsonResponse({'status': 'error', 'message': 'No associated dates found'}, status=404)

        return JsonResponse({'status': 'success'})
    except PEP_Entities.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Entity not found'}, status=404)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
