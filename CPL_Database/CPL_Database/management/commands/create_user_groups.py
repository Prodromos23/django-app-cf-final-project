from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from pep.models import PEP_Entities, PEP_Names  # Import models as needed


# 3 GROUPS INCLUDING SUPERUSER
# GROUP1: 

class Command(BaseCommand):
    help = 'Create user groups with specific permissions'

    def handle(self, *args, **kwargs):
        # Create or get the groups
        group1, created = Group.objects.get_or_create(name='Group1')
        group2, created = Group.objects.get_or_create(name='Group2')

        # Define permissions for Group1 (add, change, view)
        permissions_group1 = [
            Permission.objects.get(codename='add_pep_entities'),
            Permission.objects.get(codename='change_pep_entities'),
            Permission.objects.get(codename='view_pep_entities'),
            Permission.objects.get(codename='add_pep_names'),
            Permission.objects.get(codename='change_pep_names'),
            Permission.objects.get(codename='view_pep_names'),
            Permission.objects.get(codename='add_pep_dates'),
            Permission.objects.get(codename='change_pep_dates'),
            Permission.objects.get(codename='view_pep_dates'),
            Permission.objects.get(codename='add_pep_entities_subfund'),
            Permission.objects.get(codename='change_pep_entities_subfund'),
            Permission.objects.get(codename='view_pep_entities_subfund'),

            Permission.objects.get(codename='add_pep_entities_names'),
            Permission.objects.get(codename='change_pep_entities_names'),
            Permission.objects.get(codename='view_pep_entities_names'),
            Permission.objects.get(codename='add_pep_info'),
            Permission.objects.get(codename='change_pep_info'),
            Permission.objects.get(codename='view_pep_info'),
            
            Permission.objects.get(codename='add_pep_estimations'),
            Permission.objects.get(codename='change_pep_estimations'),
            Permission.objects.get(codename='view_pep_estimations'),
            Permission.objects.get(codename='add_pep_classifications'),
            Permission.objects.get(codename='change_pep_classifications'),
            Permission.objects.get(codename='view_pep_classifications'),

            Permission.objects.get(codename='add_fund'),
            Permission.objects.get(codename='change_fund'),
            Permission.objects.get(codename='view_fund'),

            Permission.objects.get(codename='add_subfund'),
            Permission.objects.get(codename='change_subfund'),
            Permission.objects.get(codename='view_subfund'),

            Permission.objects.get(codename='add_pep_nationality'),
            Permission.objects.get(codename='change_pep_nationality'),
            Permission.objects.get(codename='view_pep_nationality'),

            Permission.objects.get(codename='add_person_reviewers'),
            Permission.objects.get(codename='change_person_reviewers'),
            Permission.objects.get(codename='view_person_reviewers'),

            Permission.objects.get(codename='add_serviceprovidertype'),
            Permission.objects.get(codename='change_serviceprovidertype'),
            Permission.objects.get(codename='view_serviceprovidertype'),

            # COI_Dates,COI_Cases,COI_Cases_Subfund,COI_Info,COI_Status
            Permission.objects.get(codename='add_coi_status'),
            Permission.objects.get(codename='change_coi_status'),
            Permission.objects.get(codename='view_coi_status'),

            Permission.objects.get(codename='add_coi_dates'),
            Permission.objects.get(codename='change_coi_dates'),
            Permission.objects.get(codename='view_coi_dates'),

            Permission.objects.get(codename='add_coi_cases'),
            Permission.objects.get(codename='change_coi_cases'),
            Permission.objects.get(codename='view_coi_cases'),
            
            Permission.objects.get(codename='add_coi_cases_subfund'),
            Permission.objects.get(codename='change_coi_cases_subfund'),
            Permission.objects.get(codename='view_coi_cases_subfund'),

            Permission.objects.get(codename='add_coi_info'),
            Permission.objects.get(codename='change_coi_info'),
            Permission.objects.get(codename='view_coi_info'),
        ]
        # Define permissions for Group2 (add, view) 
        # !| Has not be defined well at the moment
        permissions_group2 = [
            Permission.objects.get(codename='add_pep_entities'),
            Permission.objects.get(codename='view_pep_entities'),
            Permission.objects.get(codename='add_pep_names'),
            Permission.objects.get(codename='view_pep_names'),
            Permission.objects.get(codename='add_pep_dates'),
            Permission.objects.get(codename='view_pep_dates'),
            Permission.objects.get(codename='add_pep_entities_names'),
            Permission.objects.get(codename='view_pep_entities_names'),
            Permission.objects.get(codename='add_pep_info'),
            Permission.objects.get(codename='view_pep_info'),

            # COI_Dates,COI_Cases,COI_Cases_Subfund,COI_Info,COI_Status
            Permission.objects.get(codename='add_coi_status'),
            Permission.objects.get(codename='view_coi_status'),

            Permission.objects.get(codename='add_coi_dates'),
            Permission.objects.get(codename='view_coi_dates'),

            Permission.objects.get(codename='add_coi_cases'),
            Permission.objects.get(codename='view_coi_cases'),
            
            Permission.objects.get(codename='add_coi_cases_subfund'),
            Permission.objects.get(codename='view_coi_cases_subfund'),

            Permission.objects.get(codename='add_coi_info'),
            Permission.objects.get(codename='view_coi_info'),
        ]
        # Assign permissions to groups
        group1.permissions.set(permissions_group1)
        group1.save()
        group2.permissions.set(permissions_group2)
        group2.save()

        self.stdout.write(self.style.SUCCESS('Successfully created groups and assigned permissions'))


# Run the command to create the groups:
# python manage.py create_groups