from django.db import models


class Urls(models.Model):
    hashc = models.CharField(max_length=200, verbose_name='Хеш')
    url = models.URLField(verbose_name='Ссылка')
    urlRDF = models.URLField(verbose_name='Ссылка PDF', null=True, blank=True)

    def __str__(self):
          return f'{self.url}'
    class Meta:
            verbose_name = 'Ссылки'
            verbose_name_plural = 'Ссылки'

    