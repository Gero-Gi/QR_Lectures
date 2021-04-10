from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

from .managers import LectureManager
from django.contrib.auth import get_user_model
import string, random

User = get_user_model()

class GeoPosition(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return '{}-{}'.format(self.latitude, self.longitude)

    def compare(self, geo_pos, threshold):
        pass  # todo


class Department(models.Model):
    name = models.CharField(max_length=150)
    geo_position = models.ForeignKey(
        GeoPosition, null=True, on_delete=SET_NULL)

    def __str__(self):
        return self.name


class Lecture(models.Model):
    professor = models.ForeignKey('auth_app.User', on_delete=CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=SET_NULL, null=True)

    start_at = models.DateTimeField()

    # to set later
    started_at = models.DateTimeField(null=True, blank=True, default=None)
    ended_at = models.DateTimeField(null=True, blank=True, default=None)
    # for qr-code
    start_code = models.CharField(max_length=10, blank=True)
    end_code = models.CharField(max_length=10, blank=True)


    objects = LectureManager()

    def __str__(self):
        return self.name

    @property
    def engagement(self):
        return self.get_engagement()

    @property
    def students(self):
        return len(self.get_students())

    def get_engagement(self):
        sessions = Session.objects.filter(lecture=self)
        total = len(sessions)
        if total == 0: return 0
        sum = 0
        for s in sessions:
            if s.is_completed:
                sum += 1
        return sum/total

    def get_students(self):
        sessions = Session.objects.filter(lecture=self) 
        return [s.student for s in sessions]   

    def refresh_start(self):
        self.start_code = self._get_random_code(10)
        self.save()

    def refresh_end(self):
        self.end_code = self._get_random_code(10)
        self.save()

    def _get_random_code(self, len):
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(0,len)])


class Session(models.Model):
    student = models.ForeignKey('auth_app.User', on_delete=CASCADE)
    lecture = models.ForeignKey(Lecture, on_delete=CASCADE)
    geo_posititon = models.ForeignKey(
        GeoPosition, on_delete=SET_NULL, null=True)

    start_at = models.DateTimeField()
    end_at = models.DateTimeField(null=True, blank=True)

    is_completed = models.BooleanField(default=False)
    

    def __str__(self):
        return '{}-{}'.format(self.student.id, self.lecture.name)

