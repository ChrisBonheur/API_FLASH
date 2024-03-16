from collections.abc import Iterable
from django.db import models
from django.contrib.auth.models import User


class AcademicYear(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    year_name = models.CharField(max_length=10, unique=True)
    year_begin = models.SmallIntegerField(default=0)
    year_end = models.SmallIntegerField(default=0)
    users = models.ManyToManyField(User, related_name='years')

    def __str__(self) -> str:
        return self.year_name if self.year_name else "Année Académique"
    
    class Meta:
        verbose_name = "Année Académique"
        constraints = [
            models.UniqueConstraint(fields=['year_begin', "year_end"], name="unique_year_academic")
        ]
        ordering = ["-year_end"]

    def save(self, *args, **kwargs):
        self.year_name = f"{self.year_begin}-{self.year_end}"
        return super(AcademicYear, self).save(*args, **kwargs)