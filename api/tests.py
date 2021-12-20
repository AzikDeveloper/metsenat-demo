from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from api.models import Sponsor


class SponsorTests(APITestCase):

    def test_create_sponsor(self):
        url = reverse('api:sponsors')
        data = {
            'full_name': 'Testov Test Testovich',
            'phone_number': '+998996676767',
            'money': 13000000,
            'person_type': 'juridic',
            'company_name': 'Max way'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sponsor.objects.count(), 2)
        self.assertEqual(Sponsor.objects.get().full_name, 'Testov Test Testovich')
