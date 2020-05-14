from django.contrib.auth.models import User, Group
from django.test import TestCase

from djop.models import ObjectPermission
from tests.models import City


class DjopTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.city1 = City.objects.create(name="Amsterdam")
        cls.city1_permission = ObjectPermission.objects.create(
            "tests.view_city", obj=cls.city1)
        cls.user1 = User.objects.create(username='user1')
        cls.user2 = User.objects.create(username='user2')
        cls.user3 = User.objects.create(username='user3')

        cls.city1_permission.users.add(cls.user2)

        cls.group1 = Group.objects.create(name="group1")
        cls.city1_permission.groups.add(cls.group1)
        cls.group1.user_set.add(cls.user3)

    def test_no_object_permission(self):
        self.assertFalse(self.user1.has_perm('tests.view_city', self.city1))

    def test_user_has_object_permission(self):
        self.assertTrue(self.user2.has_perm('tests.view_city', self.city1))

    def test_group_has_object_permission(self):
        self.assertTrue(self.user3.has_perm('tests.view_city', self.city1))
