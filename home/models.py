from django.db import models

class home(models.Model)
    class Meta:
            permissions = (('can_transmission','Can enter the transmission section'),)