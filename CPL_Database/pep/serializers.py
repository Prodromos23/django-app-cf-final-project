from rest_framework import serializers
from pep.models import PEP_Names,Subfund, PEP_Entities

class PEPNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PEP_Names
        fields = ['pep_name', 'position', 'entities_id_fk']


class EntitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = PEP_Entities
        fields = ['entity_name']
