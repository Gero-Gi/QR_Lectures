from datetime import timedelta
import random
from .models import Department, Lecture, Session

from django.contrib.auth import get_user_model
User = get_user_model()
import string


from faker import Faker, providers
faker = Faker()



class FakeDatabase(object):
    departments = 4
    students = 100
    professors = 1
    lectures_per_professor = 100
    
    _min_studs = .5
    _min_engagement = .6
    

    def delete(self):
        User.objects.filter(is_superuser=False).delete()
        Department.objects.all().delete()

    def make(self):
        self.delete()
        print('faking departments...')
        self._make_departments()
        print('faking professors...')
        self._make_professors()
        print('faking students...')
        self._make_students()
        print('faking lectures...')
        self._make_lectures()
        print('faking sessions...')
        self._make_sessions()
        print('completed.')
    
    def _make_departments(self):
        for i in range(self.departments):
            Department.objects.create(
                name=faker.sentence(nb_words=3)
                # todo geolocation
            )

    def _make_students(self):
        for i in range(0, self.students):
            first_name = faker.first_name()
            last_name = faker.last_name()
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email='{}.{}@studenti.it'.format(first_name, last_name).lower(),
            )
            user.set_password('password')
            user.save()



    def _make_professors(self):
        for i in range(0, self.professors):
            first_name = faker.first_name()
            last_name = faker.last_name()
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                email='{}.{}@prof.it'.format(first_name, last_name).lower(),
                is_professor=True,
            )
            user.set_password('password')
            user.save()

    def _get_random_department(self):
        d = Department.objects.all()
        return d[random.randint(0, len(d)-1)]

    def _get_random_code(self, len):
        return ''.join([random.choice(string.ascii_letters + string.digits) for i in range(0,len)])


    def _make_lectures(self):
        for professor in User.objects.filter(is_professor=True):
            for i in range(0,self.lectures_per_professor):
                if random.random() < .85:
                    start = faker.date_time_between(start_date='-1y', end_date='now')
                    started_at = start
                    end = start + timedelta(hours=2)
                else:
                    start = faker.date_time_between(start_date='now', end_date='+2M')
                    started_at = None
                    end = None

                Lecture.objects.create(
                    professor=professor,
                    name=faker.paragraph(nb_sentences=1),
                    description=faker.paragraph(nb_sentences=8),
                    start_at=start,
                    started_at=started_at,
                    ended_at = end,
                    department=self._get_random_department(),
                    start_code=self._get_random_code(10),
                    end_code=self._get_random_code(10),
                )


   
        
    def _make_sessions(self):
        for student in User.objects.filter(is_professor=False):
            for lecture in Lecture.objects.all():
                if not lecture.started_at: continue
                if random.random() > self._min_studs: continue
                end_at =  None if random.random() > self._min_engagement else lecture.ended_at
                Session.objects.create(
                    student=student,
                    lecture=lecture,
                    start_at=lecture.started_at,
                    end_at =end_at,
                    is_completed=end_at != None
                )






