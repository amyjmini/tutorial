from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_delete


class FileModel(models.Model):
    file = models.FileField(blank=True, null=True)

@receiver(post_delete, sender=FileModel)
def submission_delete(sender, instance, **kwargs):
    """
    This function is used to delete attachments when a file object is deleted.
    Django does not do this automatically.
    """
    instance.file.delete(False)