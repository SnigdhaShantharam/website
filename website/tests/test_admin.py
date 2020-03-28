from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            phone_number=9538597732,
            password='password123'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            phone_number=9449398172,
            password='test123',
            name='Test User Full Name',
        )

    def test_for_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:users_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.phone_number)
        self.assertContains(res, self.user.name)

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse('admin:users_user_change', args=[self.user.id])
        # /admin/users/user/id/
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test create user page works"""
        url = reverse('admin:users_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
