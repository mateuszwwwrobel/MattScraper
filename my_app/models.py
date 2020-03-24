from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    #Instead of Search object() show an actual search thing.
    def __str__(self):
         return '{}'.format(self.search)

    #change a plural form of search in admin view.
    class Meta:
         verbose_name_plural = "Searches"
