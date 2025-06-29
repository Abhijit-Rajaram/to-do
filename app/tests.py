from django.test import TestCase
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username="ci_user", password="pass")
        self.assertEqual(user.username, "ci_user")