from django.core.exceptions import ObjectDoesNotExist
from django.db.models import query
from rest_framework import serializers

from lectures.models import Lecture, Session


class LectureSerializer(serializers.ModelSerializer):
    has_attended = serializers.SerializerMethodField()
    start_only = serializers.SerializerMethodField()

    professor = serializers.SerializerMethodField()
    department = serializers.SerializerMethodField()

    class Meta:
        model = Lecture
        exclude = ['start_code', 'end_code']
        

    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def get_has_attended(self, obj):
        try:
            session = Session.objects.filter(lecture=obj)
            session = session.get(student=self._user)
            return session.is_completed
        except ObjectDoesNotExist:
            return False

    def get_start_only(self, obj):
        try:
            session = Session.objects.filter(lecture=obj)
            session = session.get(student=self._user)
            return not session.is_completed
        except ObjectDoesNotExist:
            return False

    
    @staticmethod
    def get_professor(obj):
        return str(obj.professor) 
    
    @staticmethod
    def get_department(obj):
        return str(obj.department)
