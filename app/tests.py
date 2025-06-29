from django.test import TestCase
from django.contrib.auth.models import User

class SimpleTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(username="ci_user", password="pass")
        self.assertEqual(user.username, "ci_user")

"""
        **** Just addded to check whether a failing test breaks the integration or not ****
        
class FailingTest(TestCase):
    def test_fail_intentionally(self):
        self.assertEqual(1, 0, "This test is supposed to fail and break CI")
"""
