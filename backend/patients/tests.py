from rest_framework import status
from rest_framework.test import APITestCase


class PatientAPITests(APITestCase):
    """Full CRUD + validation tests for /api/patients/."""

    URL = "/api/patients/"

    def setUp(self):
        """Create a baseline patient for retrieve/update/delete tests."""
        self.patient_data = {
            "name": "John Doe",
            "age": 30,
            "gender": "male",
            "phone": "9876543210",
            "address": "123 Main St",
        }
        resp = self.client.post(self.URL, self.patient_data, format="json")
        self.patient_id = resp.data["id"]
        self.detail_url = f"{self.URL}{self.patient_id}/"

    # ---- Happy-path CRUD ----

    def test_create_valid_patient(self):
        """POST with valid data returns 201."""
        data = {**self.patient_data, "phone": "1111111111"}
        resp = self.client.post(self.URL, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_list_patients(self):
        """GET list returns 200 with at least one patient."""
        resp = self.client.get(self.URL)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data), 1)

    def test_retrieve_patient(self):
        """GET detail returns 200."""
        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["name"], "John Doe")

    def test_put_update(self):
        """PUT full update returns 200."""
        data = {**self.patient_data, "name": "John Updated", "age": 31}
        resp = self.client.put(self.detail_url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["name"], "John Updated")

    def test_patch_update(self):
        """PATCH partial update returns 200."""
        resp = self.client.patch(self.detail_url, {"age": 32}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["age"], 32)

    def test_delete_patient(self):
        """DELETE returns 204, then GET returns 404."""
        resp = self.client.delete(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        resp = self.client.get(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # ---- Validation failures ----

    def test_duplicate_phone(self):
        """POST with an already-used phone returns 400."""
        data = {**self.patient_data, "name": "Another Person"}
        resp = self.client.post(self.URL, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", resp.data)

    def test_name_with_digits(self):
        """POST with digits in name returns 400."""
        data = {**self.patient_data, "name": "John123", "phone": "2222222222"}
        resp = self.client.post(self.URL, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("name", resp.data)

    def test_age_over_120(self):
        """POST with age 150 returns 400."""
        data = {**self.patient_data, "age": 150, "phone": "3333333333"}
        resp = self.client.post(self.URL, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("age", resp.data)

    def test_phone_nine_digits(self):
        """POST with a 9-digit phone returns 400."""
        data = {**self.patient_data, "phone": "123456789"}
        resp = self.client.post(self.URL, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", resp.data)

    def test_invalid_gender(self):
        """POST with gender 'alien' returns 400."""
        data = {**self.patient_data, "gender": "alien", "phone": "4444444444"}
        resp = self.client.post(self.URL, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("gender", resp.data)

    def test_missing_required_fields(self):
        """POST with empty body returns 400 for all required fields."""
        resp = self.client.post(self.URL, {}, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        for field in ("name", "age", "gender", "phone"):
            self.assertIn(field, resp.data)

    def test_blank_address_allowed(self):
        """POST with no address returns 201 (address is optional)."""
        data = {"name": "No Address", "age": 40, "gender": "other", "phone": "5555555555"}
        resp = self.client.post(self.URL, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["address"], "")
