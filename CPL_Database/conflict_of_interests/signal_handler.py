from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import COI_Info, COI_Dates

@receiver(post_save, sender=COI_Info)
def update_pep_dates(sender, instance, **kwargs):
    coi_dates = instance.pep_dates_id_fk
    coi_dates.date_updated_last = timezone.now().date()
    coi_dates.save()