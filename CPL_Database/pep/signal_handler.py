from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import PEP_Info, PEP_Dates

@receiver(post_save, sender=PEP_Info)
def update_pep_dates(sender, instance, **kwargs):
    pep_dates = instance.pep_dates_id_fk
    pep_dates.date_updated_last = timezone.now().date()
    pep_dates.save()