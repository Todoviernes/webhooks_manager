from django.db import models
from webhooks_manager.utils.models import ManagerModel, SlugModel

# Create your models here.
class Source(ManagerModel, SlugModel):
    url = models.URLField(max_length=200)

    def __str__(self):
        return self.name

class Webhook(ManagerModel):
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    data = models.JSONField()

    def __str__(self):
        return self.name
