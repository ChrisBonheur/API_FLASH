from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from academic_years.models import AcademicYear
from config_global.models import Country, Town
from . models import Teacher
import json


class TeacherTestCase(APITestCase):
    url = reverse_lazy('teacher-list')

    def setUp(self) -> None:
        self.country = Country.objects.create(code="CG", label="Congo", nationality_label="Congolaise", ordering=1)
        self.city = Town.objects.create(code="PN", label="Pointe-Noire", country=self.country, ordering=1)
        user = User.objects.create(username="bonheur2", last_name="bonheur", first_name="maf", email="bonheur@gmail.com", password="1234")
        self.data = {
            "user": user,
            "birth_city": self.city,
            "nationality": self.country,
            "town_residence": self.city,
            "civility": "homme",
            "birth_date": "2023-02-24",
            "contact": "068314433",
        }
        self.teacher = Teacher.objects.create(**self.data)
        self.year  = AcademicYear.objects.create(
            year_name="2023-2024",
            year_begin="2023",
            year_end="2024"
        )
        return super().setUp()

    def test_save(self):
        self.client.force_authenticate(self.teacher.user)
        data = {
            "username": "bonheur",
            "last_name": "bonheur",
            "first_name": "maf",
            "email": "bonheur@gmail.com",
            "birth_city": self.city.id,
            "nationality": self.country.id,
            "town_residence": self.city.id,
            "civility": "homme",
            "birth_date": "2023-02-24",
            "contact": "068314433",
        }
        headers = {
            'ACADEMIC-YEAR-ID': '1'
        }

        res = self.client.put(f"{self.url}{self.teacher.id}/", json=data, headers={'ACADEMIC-YEAR-ID': f"{self.year.id}"})
        import pdb;pdb.set_trace()
        count_before = Teacher.objects.count()
        res = self.client.post(self.url, data=data)
        count_after = Teacher.objects.count()
        self.assertEqual(count_after, count_before + 1)
        self.assertEqual(res.status_code, 201)


    def test_update(self):
        self.client.force_authenticate(self.teacher.user)
        data = {
            "username": "chris",
            "last_name": "AJO",
            "first_name": "Maf",
            "email": "bonheur@gmail.com",
            "birth_city": self.city.id,
            "nationality": self.country.id,
            "town_residence": self.city.id,
            "civility": "homme",
            "birth_date": "2023-02-24",
            "contact": "068314433",
        }
        headers = {
            'ACADEMIC-YEAR-ID': f"{self.year.id}"
        }

        res = self.client.put(f"{self.url}{self.teacher.id}/", data=data, headers={'headers': {
            'ACADEMIC-YEAR-ID': f"{self.year.id}"
        }})
        res_json = json.loads(res.content)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['username'], res_json['username'])
        self.assertEqual(data['last_name'], res_json['last_name'])
        self.assertEqual(data['first_name'], res_json['first_name'])
