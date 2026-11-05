from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

LOGIN_URL = "/api/auth/login/"
REGISTER_URL = "/api/auth/register/"
PATIENTS_URL = "/api/patients/"

PATIENT = {
    "name": "Anu Mathew",
    "age": 34,
    "gender": "female",
    "phone": "9876543210",
    "address": "Kollam",
}


def new_user_data(**overrides):
    data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "password": "Strong1234",
        "role": "receptionist",
    }
    data.update(overrides)
    return data


class LoginTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username="rec1", email="rec1@example.com",
            password="Pass12345", role="receptionist",
        )

    def test_login_success_returns_tokens(self):
        resp = self.client.post(
            LOGIN_URL, {"username": "rec1", "password": "Pass12345"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn("access", resp.data)
        self.assertIn("refresh", resp.data)

    def test_login_wrong_password_is_401(self):
        resp = self.client.post(
            LOGIN_URL, {"username": "rec1", "password": "wrong"}, format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_real_token_grants_access(self):
        """Uses a real JWT, which also checks the REST_FRAMEWORK settings."""
        resp = self.client.post(
            LOGIN_URL, {"username": "rec1", "password": "Pass12345"}, format="json"
        )
        token = resp.data["access"]
        resp = self.client.get(PATIENTS_URL, HTTP_AUTHORIZATION=f"Bearer {token}")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_no_token_is_401(self):
        resp = self.client.get(PATIENTS_URL)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)


class RolePermissionTests(APITestCase):
    def make_client(self, role):
        user = User.objects.create_user(
            username=f"{role}1", email=f"{role}1@example.com",
            password="Pass12345", role=role,
        )
        self.client.force_authenticate(user=user)

    def test_receptionist_can_create_patient(self):
        self.make_client("receptionist")
        resp = self.client.post(PATIENTS_URL, PATIENT, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_admin_can_create_patient(self):
        self.make_client("admin")
        resp = self.client.post(PATIENTS_URL, PATIENT, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_doctor_can_view_patients(self):
        self.make_client("doctor")
        resp = self.client.get(PATIENTS_URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_doctor_cannot_create_patient(self):
        self.make_client("doctor")
        resp = self.client.post(PATIENTS_URL, PATIENT, format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)


class RegisterTests(APITestCase):
    def login_as(self, role):
        user = User.objects.create_user(
            username=f"{role}1", email=f"{role}1@example.com",
            password="Pass12345", role=role,
        )
        self.client.force_authenticate(user=user)

    def test_admin_can_register_user(self):
        self.login_as("admin")
        resp = self.client.post(REGISTER_URL, new_user_data(), format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_non_admin_cannot_register(self):
        self.login_as("receptionist")
        resp = self.client.post(REGISTER_URL, new_user_data(), format="json")
        self.assertEqual(resp.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_cannot_register(self):
        resp = self.client.post(REGISTER_URL, new_user_data(), format="json")
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_fields(self):
        self.login_as("admin")
        resp = self.client.post(REGISTER_URL, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_short_password(self):
        self.login_as("admin")
        resp = self.client.post(
            REGISTER_URL, new_user_data(password="Ab1"), format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", resp.data)

    def test_all_digit_password(self):
        self.login_as("admin")
        resp = self.client.post(
            REGISTER_URL, new_user_data(password="12345678"), format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", resp.data)

    def test_invalid_role(self):
        self.login_as("admin")
        resp = self.client.post(
            REGISTER_URL, new_user_data(role="janitor"), format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("role", resp.data)

    def test_invalid_email(self):
        self.login_as("admin")
        resp = self.client.post(
            REGISTER_URL, new_user_data(email="not-an-email"), format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", resp.data)

    def test_duplicate_username(self):
        self.login_as("admin")
        self.client.post(REGISTER_URL, new_user_data(), format="json")
        resp = self.client.post(
            REGISTER_URL, new_user_data(email="other@example.com"), format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", resp.data)

    def test_duplicate_email(self):
        self.login_as("admin")
        self.client.post(REGISTER_URL, new_user_data(), format="json")
        resp = self.client.post(
            REGISTER_URL, new_user_data(username="another"), format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", resp.data)


class SuperuserRoleTest(APITestCase):
    def test_superuser_gets_admin_role(self):
        user = User.objects.create_superuser(
            username="root", email="root@example.com", password="Pass12345"
        )
        self.assertEqual(user.role, "admin")