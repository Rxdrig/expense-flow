from datetime import date

from ..models import Expense

SPANISH_MONTHS = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]


def filter_expenses_for_report(user, filters):
    expenses = Expense.objects.filter(user=user).select_related("recurrence_parent")

    if filters.get("scope") == "all":
        return expenses

    date_start = filters.get("date_start")
    date_end = filters.get("date_end")
    category = filters.get("category")

    if date_start:
        expenses = expenses.filter(date__gte=date_start)
    if date_end:
        expenses = expenses.filter(date__lte=date_end)
    if category:
        expenses = expenses.filter(category=category)

    return expenses


def build_report_filename(user, extension, report_date=None):
    report_date = report_date or date.today()
    month_name = SPANISH_MONTHS[report_date.month - 1]
    safe_extension = extension.lstrip(".")
    return f"ExpenseFlow_Reporte_{month_name}_{report_date.year}.{safe_extension}"
