from datetime import datetime, time
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from rest_framework import response
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from lectures.models import Lecture, Session

from .serializers import LectureSerializer

class LectureViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = LectureSerializer
    http_method_names = ['get']

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
        kwargs['user'] = self.request.user
        return serializer_class(*args, **kwargs)

    def get_queryset(self):
        queryset = Lecture.objects.all().order_by('-start_at')
        type = self.request.query_params.get('filter', None)
        if type == 'upcoming':
            queryset = queryset.filter(started_at__isnull=True)
        elif type != None:
            sessions = Session.objects.filter(student=self.request.user).order_by('-start_at')
            if type == 'start_only':
                sessions = sessions.filter(end_at__isnull=True).order_by('-start_at')
                queryset = [x.lecture for x in sessions]
            elif type == 'completed':
                sessions = sessions.filter(end_at__isnull=False).order_by('-start_at')
                queryset = [x.lecture for x in sessions]

        return queryset



class SessionView(APIView):
    http_method_names = ['post']

    def post(self, request, *args, **kwargs):
        lec_pk = kwargs.get('lecture_pk', None)
        if lec_pk == None: return Response({'msg': 'missing lecture parameter in url'}, status=HTTP_400_BAD_REQUEST)
        
        code = self.request.data.get('code', None)

        if code == None:return Response({'msg': 'missing code'}, status=HTTP_400_BAD_REQUEST)
        
        try:
            lecture = Lecture.objects.get(id=lec_pk)
        except ObjectDoesNotExist:
            return Response(status=HTTP_404_NOT_FOUND)

        try:
            session = Session.objects.filter(lecture=lecture)
            session = session.get(student=self.request.user)
            if lecture.end_code == code:
                session.end_at = datetime.now()
                session.is_completed = True
                session.save()
                return Response(LectureSerializer(lecture, user=self.request.user).data, 200)
            else:
                return Response(status=HTTP_403_FORBIDDEN)
        except:
            if lecture.start_code == code:
                session = Session.objects.create(
                    lecture=lecture,
                    student=self.request.user,
                    start_at=datetime.now()
                )
                return Response(LectureSerializer(lecture, user=self.request.user).data, 200)
            else:
                return Response(status=HTTP_403_FORBIDDEN)
        

