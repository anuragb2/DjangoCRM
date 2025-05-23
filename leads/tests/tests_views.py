from django.test import TestCase
from django.shortcuts import reverse

# Create your tests here.


class LandingPageTest(TestCase):

    def test_get(self):
        response = self.client.get(reverse("lead-landing"))
        print(response.status_code)
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,"landing.html")
