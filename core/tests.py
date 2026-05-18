from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Expense


class ExpenseAccessTests(TestCase):
	def setUp(self):
		self.user1 = User.objects.create_user(username="user1", password="test12345")
		self.user2 = User.objects.create_user(username="user2", password="test12345")
		self.expense = Expense.objects.create(
			user=self.user1,
			title="Lunch",
			amount=Decimal("10.50"),
			category=Expense.CATEGORY_FOOD,
			date="2026-05-12",
		)

	def test_dashboard_requires_login(self):
		response = self.client.get(reverse("index"))
		self.assertEqual(response.status_code, 302)
		self.assertIn(reverse("login"), response.url)

	def test_user_cannot_access_another_users_expense(self):
		self.client.login(username="user2", password="test12345")
		response = self.client.get(reverse("expense_detail", args=[self.expense.id]))
		self.assertEqual(response.status_code, 404)
