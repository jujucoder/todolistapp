from rest_framework.test import APITestCase
from authentication.models import User


class TestModel(APITestCase):
    def test_create_user(self):
        user=User.objects.create_user('user','user@mail.com','foo')
        self.assertIsInstance(user,User)
        self.assertEqual(user.email,'user@mail.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


    def test_create_superuser(self):
        user=User.objects.create_superuser('user','user@mail.com','foo')
        self.assertIsInstance(user,User)
        self.assertEqual(user.email,'user@mail.com')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


    def test_raises_error_when_no_usernameis_supplied(self):
        self.assertRaises(
            ValueError,
            User.objects.create_user,
            username="",
            email="adedireadedapo19@gmail.com",
            password="iamabillionaire24434",
        )
        self.assertRaisesMessage(ValueError,'The given username must be set')

    def test_raises_error_when_no_emailis_supplied(self):
        self.assertRaises(
            ValueError,
            User.objects.create_user,
            username="dapoadedire",
            email="",
            password="iamabillionaire24434",
        )
        self.assertRaisesMessage(ValueError, "The given email must be set")

    def test_raises_error_with_message_when_no_username_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given username must be set"):
            User.objects.create_user(
                username="",
                email="adedireadedapo19@gmail.com",
                password="iamabillionaire24434",
            )

    def test_raises_error_with_message_when_no_email_is_supplied(self):
        with self.assertRaisesMessage(ValueError, "The given email must be set"):
            User.objects.create_user(
                username="dapoadedire", email="", password="iamabillionaire24434"
            )

    # def test_create_super_user_with_super_user_status(self):
    #     user = User.objects.create_superuser('dapoadedire', 'adedireadedapo19@gmail.com', 'iamabillionaire24434', is_staff = True)
    #     self.assertRaises(ValueError, user, 'Superuser must have is_staff=True.')

    def test_cant_create_super_user_with_super_user_status(self):
        with self.assertRaisesMessage(
            ValueError, "Superuser must have is_superuser=True."
        ):
            User.objects.create_superuser(
                username="dapoadedire",
                email="",
                password="iamabillionaire24434",
                is_superuser=False,
            )

    def test_cant_create_super_user_with_staff_status(self):
        with self.assertRaisesMessage(ValueError, "Superuser must have is_staff=True."):
            User.objects.create_superuser(
                username="dapoadedire",
                email="",
                password="iamabillionaire24434",
                is_staff=False,
            )


# coverage run manage.py test && coverage report && coverage html