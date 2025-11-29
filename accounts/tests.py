from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase


class IndexViewTests(TestCase):
	def test_index_returns_success(self):
		url = reverse("accounts:index")
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)


class SignupViewTests(TestCase):
	def setUp(self):
		self.url = reverse("accounts:signup")

	def test_signup_creates_user_and_logs_in(self):
		signup_data = {
			"account_id": "user001",
			"email": "user001@example.com",
			"first_name": "Taro",
			"last_name": "Yamada",
			"birth_date": "2000-01-01",
			"password1": "StrongPass123",
			"password2": "StrongPass123",
		}

		response = self.client.post(self.url, signup_data)

		self.assertRedirects(response, reverse("accounts:index"))

		user_model = get_user_model()
		self.assertTrue(user_model.objects.filter(account_id="user001").exists())

		session_user_id = self.client.session.get("_auth_user_id")
		self.assertEqual(str(user_model.objects.get(account_id="user001").pk), session_user_id)

	def test_signup_with_mismatched_passwords_shows_errors(self):
		signup_data = {
			"account_id": "user002",
			"email": "user002@example.com",
			"first_name": "Hanako",
			"last_name": "Suzuki",
			"birth_date": "2001-02-02",
			"password1": "StrongPass123",
			"password2": "DifferentPass456",
		}

		response = self.client.post(self.url, signup_data)

		self.assertEqual(response.status_code, 200)

		form = response.context["form"]
		self.assertIn("password2", form.errors)
		self.assertIn(form.error_messages["password_mismatch"], form.errors["password2"])

		user_model = get_user_model()
		self.assertFalse(user_model.objects.filter(account_id="user002").exists())


class LoginLogoutViewTests(TestCase):
	def setUp(self):
		user_model = get_user_model()
		self.user = user_model.objects.create_user(
			account_id="login001",
			email="login001@example.com",
			password="LoginPass123",
		)

	def test_login_redirects_to_shoppinglist(self):
		url = reverse("accounts:login")
		response = self.client.post(url, {"username": "login001", "password": "LoginPass123"})

		self.assertRedirects(response, reverse("shoppinglist:list"))
		self.assertEqual(str(self.user.pk), self.client.session.get("_auth_user_id"))

	def test_login_with_invalid_credentials_shows_errors(self):
		url = reverse("accounts:login")
		response = self.client.post(url, {"username": "login001", "password": "WrongPassword"})

		self.assertEqual(response.status_code, 200)
		form = response.context["form"]
		self.assertTrue(form.non_field_errors())
		expected_message = form.error_messages["invalid_login"] % {
			"username": form.username_field.verbose_name
		}
		self.assertIn(expected_message, list(form.non_field_errors()))
		self.assertIsNone(self.client.session.get("_auth_user_id"))

	def test_logout_logs_out_user(self):
		self.client.login(account_id="login001", password="LoginPass123")

		url = reverse("accounts:logout")
		response = self.client.get(url)

		self.assertRedirects(response, reverse("accounts:index"))
		self.assertIsNone(self.client.session.get("_auth_user_id"))
