from django.db import models
import datetime

from django.db.models.aggregates import Count
from django.db.models.query_utils import FilteredRelation, Q


class LectureQueryset(models.QuerySet):
    def latest(self, years=0, months=0, days=0, hours=0):
        now = datetime.datetime.now()
        days = years * 360 + months * 30 + days
        min = now - datetime.timedelta(days=days, hours=hours)
        return self.filter(started_at__range=(min, now))

    def engagement(self, **kwargs):
        query = self.latest(**kwargs)
        return sorted(query, key= lambda t: -t.engagement)

class LectureManager(models.Manager):
    def get_queryset(self):
        return LectureQueryset(self.model, using=self._db)

    def get_latest(self, professor, **kwargs):
        return self.by_professor(professor).latest(**kwargs).order_by('start_at')

    def get_latest_eng(self, professor, **kwargs):
        return self.by_professor(professor).engagement(**kwargs)

    def by_professor(self, professor):
        return self.get_queryset().filter(professor=professor)
