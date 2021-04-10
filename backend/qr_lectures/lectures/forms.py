from django.db.models import fields
from django import forms

from .models import Department, Lecture

class LectureForm(forms.ModelForm):
    start_at = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input',
            'data-target': '#start_at'
        })
    )


    department = forms.ModelChoiceField(queryset=Department.objects.all())

    class Meta:
        model = Lecture
        fields = ['name', 'description', 'start_at', 'department']


    def __init__(self, *args, **kwargs):
        self._user = kwargs.pop('request', None).user
        return super(LectureForm, self).__init__(*args, **kwargs)

    def save(self):
        self.instance.professor = self._user
        return super().save()