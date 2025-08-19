from django.db import models, transaction

class MultiDBSaveMixin(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Save to the default database
        super(MultiDBSaveMixin, self).save(*args, **kwargs)
        # Save to the secondary database
        kwargs['using'] = 'secondary'
        super(MultiDBSaveMixin, self).save(*args, **kwargs)
