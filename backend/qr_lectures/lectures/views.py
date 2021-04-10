from django.http import request
from django.http.response import Http404, HttpResponseForbidden
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView

from .forms import LectureForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Lecture, Session
from .charts import EngagementChart, StudCountChart, StudCountDataSet
import datetime
import random
import string
import json
from django.urls import reverse


def test_user(request, user):
    if request.user == user:
        return True
    return False


class DashBoardView(LoginRequiredMixin, TemplateView):
    template_name = 'lectures/dashboard_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query_charts = Lecture.objects.get_latest(
            self.request.user, months=2).exclude(ended_at__isnull=True)
        context['eng_chart'] = EngagementChart(query_charts)
        context['stud_chart'] = StudCountChart(query_charts)

        context['top_eng'] = Lecture.objects.get_latest_eng(
            self.request.user, months=2)[:11]
        context['last'] = Lecture.objects.by_professor(self.request.user).filter(
            ended_at__isnull=True).order_by('start_at')[:5]

        return context


class LectureView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'lectures/lecture_detail.html'
    queryset = Lecture.objects.all()
    context_object_name = 'lecture'
    http_method_names = ['get', 'post']

    def test_func(self):
        return test_user(self.request, self.get_object().professor)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        sessions = Session.objects.filter(lecture=self.get_object())

        context['completed'] = [x.student for x in sessions if x.is_completed]
        context['completed'] = sorted(
            context['completed'], key=lambda t: t.last_name)
        context['start_only'] = [
            x.student for x in sessions if not x.is_completed]
       

        return context

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        if 'start' in request.POST:
            obj.started_at = datetime.datetime.now()
            # todo set IP
        elif 'end' in request.POST:
            obj.ended_at = datetime.datetime.now()


        obj.save()
        return self.get(self, request, *args, **kwargs)


class QRStart(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'lectures/qr_view.html'
    queryset = Lecture.objects.all()
    context_object_name = 'lecture'

    def test_func(self):
        return test_user(self.request, self.get_object().professor)
    
    def get(self, request, *args, **kwargs):
        self.get_object().refresh_start()
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = self.get_object()
        qr = {
            'url': reverse('session_api', kwargs={'lecture_pk': self.object.id}),
            'code': obj.start_code
        }

        ctx['qr'] = json.dumps(qr)
        ctx['info'] = 'QR Inizio Lezione'
        return ctx


class QREnd(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'lectures/qr_view.html'
    queryset = Lecture.objects.all()
    context_object_name = 'lecture'

    def test_func(self):
        return test_user(self.request, self.get_object().professor)

    def get(self, request, *args, **kwargs):
        self.get_object().refresh_end()
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        obj = self.get_object()
        qr = {
            'url': reverse('session_api', kwargs={'lecture_pk': self.object.id}),
            'code': obj.end_code
        }

        ctx['qr'] = json.dumps(qr)
        ctx['info'] = 'QR Termine Lezione'
        return ctx


class NewLectureView(LoginRequiredMixin, CreateView):
    form_class = LectureForm
    template_name = 'lectures/new_lecture_view.html'

    def get_form(self):
        return LectureForm(self.request.POST, self.request.FILES, request=self.request)

    def get_success_url(self):
        return reverse('lecture', kwargs={'pk': self.object.id})


class LectureListView(LoginRequiredMixin, ListView):
    template_name = 'lectures/lecture_list_view.html'
    context_object_name = 'lectures'

    def get_queryset(self):
        return Lecture.objects.filter(professor=self.request.user).order_by('-start_at')
