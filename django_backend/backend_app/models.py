from django.db import models


class Doc(models.Model):
    doc_id = models.CharField(max_length=200)
    user_id = models.IntegerField()
    note = models.CharField(max_length=2500, null=True, blank=True)
    bookmarked = models.BooleanField(default=False)
    last_updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['last_updated']
        unique_together = [['doc_id', 'user_id']]