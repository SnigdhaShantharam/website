from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_phone_number_successful(self):
        """Test creating a user with phone number is successful"""
        phone_number = 9538597732
        password     = 'Testpass@123'
        user         = get_user_model().objects.create_user(
            phone_number=phone_number,
            password=password
        )

        self.assertEqual(user.phone_number, phone_number)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_phone_number(self):
        """Test creating user with no phone number"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test@123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(9538597732, 'Testpass@123')

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
