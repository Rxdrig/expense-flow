from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Expense, Budget, SavingGoal

class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = ["title", "amount", "category", "date", "description", "is_recurring", "recurrence_frequency", "next_occurrence"]
        labels = {
            "title": "Título",
            "amount": "Monto",
            "category": "Categoría",
            "date": "Fecha",
            "description": "Descripción",
            "is_recurring": "Gasto recurrente",
            "recurrence_frequency": "Frecuencia",
            "next_occurrence": "Próximo gasto",
        }
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ej: Supermercado"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "min": "0"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Notas opcionales"}),
            "is_recurring": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "recurrence_frequency": forms.Select(attrs={"class": "form-control"}),
            "next_occurrence": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.setdefault("class", "form-control")
        self.fields["amount"].widget.attrs.setdefault("class", "form-control")
        self.fields["category"].widget.attrs.setdefault("class", "form-control")
        self.fields["recurrence_frequency"].required = False
        self.fields["next_occurrence"].required = False

    def clean(self):
        cleaned_data = super().clean()
        is_recurring = cleaned_data.get("is_recurring")
        recurrence_frequency = cleaned_data.get("recurrence_frequency")
        next_occurrence = cleaned_data.get("next_occurrence")

        if is_recurring and not recurrence_frequency:
            self.add_error("recurrence_frequency", "Selecciona una frecuencia para el gasto recurrente.")

        if not is_recurring:
            cleaned_data["recurrence_frequency"] = ""
            cleaned_data["next_occurrence"] = None
        elif not next_occurrence:
            cleaned_data["next_occurrence"] = cleaned_data.get("date")

        return cleaned_data


class ExpenseReportFilterForm(forms.Form):
    date_start = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Fecha inicio",
    )
    date_end = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Fecha fin",
    )
    category = forms.ChoiceField(
        required=False,
        choices=[("", "Todas las categorías")] + list(Expense.CATEGORY_CHOICES),
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Categoría",
    )
    scope = forms.ChoiceField(
        required=False,
        choices=[("all", "Todos los gastos"), ("filtered", "Solo filtrados")],
        initial="filtered",
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Alcance",
    )

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