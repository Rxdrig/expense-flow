from django.conf import settings
from django.db import models


class Expense(models.Model):
    CATEGORY_FOOD = "food"
    CATEGORY_TRANSPORT = "transport"
    CATEGORY_ENTERTAINMENT = "entertainment"
    CATEGORY_GAMES = "games"
    CATEGORY_SUBSCRIPTIONS = "subscriptions"
    CATEGORY_EDUCATION = "education"
    CATEGORY_OTHER = "other"

    CATEGORY_CHOICES = [
        (CATEGORY_FOOD, "Alimentación"),
        (CATEGORY_TRANSPORT, "Transporte"),
        (CATEGORY_ENTERTAINMENT, "Entretenimiento"),
        (CATEGORY_GAMES, "Juegos"),
        (CATEGORY_SUBSCRIPTIONS, "Suscripciones"),
        (CATEGORY_EDUCATION, "Educación"),
        (CATEGORY_OTHER, "Otro"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses",
    )
    title = models.CharField(max_length=120)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default=CATEGORY_OTHER)
    date = models.DateField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.title} - {self.amount}"


class Budget(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="budget",
    )
    monthly_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Presupuesto mensual en pesos",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Budget for {self.user.username}: ${self.monthly_budget}"


class SavingGoal(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="saving_goals",
    )
    title = models.CharField(max_length=120, help_text="Nombre de la meta (ej: Comprar PC Gamer)")
    target_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        help_text="Cantidad objetivo a ahorrar",
    )
    saved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        help_text="Cantidad ahorrada hasta ahora",
    )
    deadline = models.DateField(
        null=True,
        blank=True,
        help_text="Fecha límite opcional para cumplir la meta",
    )
    emoji = models.CharField(
        max_length=10,
        default="🎯",
        help_text="Emoji representativo de la meta",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} - {self.user.username}"

    def get_percentage(self):
        """Calcula el porcentaje completado de la meta"""
        if self.target_amount == 0:
            return 0
        percentage = (float(self.saved_amount) / float(self.target_amount)) * 100
        return min(100, round(percentage, 1))

    def get_remaining(self):
        """Calcula cuánto falta para completar la meta"""
        remaining = self.target_amount - self.saved_amount
        return max(0, remaining)