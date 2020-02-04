from django.db import models

# Create your models here.
class Sheet(models.Model):
    def __str__(self):
        return self.sheet_name
    user_sheet = models.ImageField(blank=True, null=True)