from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Expense, Budget, SavingGoal

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "date", "description"]
        labels = {
            "title": "Título",
            "amount": "Monto",
            "category": "Categoría",
            "date": "Fecha",
            "description": "Descripción",
        }
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Supermercado"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Notas opcionales"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.setdefault("class", "form-control")
        self.fields["amount"].widget.attrs.setdefault("class", "form-control")
        self.fields["category"].widget.attrs.setdefault("class", "form-control")

class BudgetForm(ModelForm):
    class Meta:
        model = Budget
        fields = ["monthly_budget"]
        labels = {
            "monthly_budget": "Presupuesto mensual ($)",
        }
        widgets = {
            "monthly_budget": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "placeholder": "Ingresa tu presupuesto mensual",
            }),
        }

class SavingGoalForm(ModelForm):
    class Meta:
        model = SavingGoal
        fields = ["title", "target_amount", "saved_amount", "deadline", "emoji"]
        labels = {
            "title": "Nombre de la meta",
            "target_amount": "Monto objetivo ($)",
            "saved_amount": "Monto ahorrado ($)",
            "deadline": "Fecha límite",
            "emoji": "Emoji",
        }
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ej: Comprar PC Gamer",
            }),
            "target_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "placeholder": "Ej: 1200000",
            }),
            "saved_amount": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "placeholder": "Cantidad ya ahorrada",
            }),
            "deadline": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date",
            }),
            "emoji": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "🎮",
                "maxlength": "10",
            }),
        }

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
        labels = {
            "username": "Usuario",
            "first_name": "Nombre",
            "last_name": "Apellido",
            "email": "Correo electrónico",
            "password1": "Contraseña",
            "password2": "Confirmar contraseña",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"