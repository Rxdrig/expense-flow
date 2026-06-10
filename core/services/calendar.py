from calendar import Calendar
from datetime import date
from decimal import Decimal

from django.utils import timezone

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


def build_month_calendar(user, year=None, month=None, category=None):
    today = timezone.localdate()
    year = year or today.year
    month = month or today.month
    month_start = date(year, month, 1)
    calendar = Calendar(firstweekday=0)
    month_days = calendar.monthdatescalendar(year, month)

    expenses = Expense.objects.filter(user=user, date__year=year, date__month=month)
    if category:
        expenses = expenses.filter(category=category)

    expenses_by_date = {}
    for expense in expenses.select_related("recurrence_parent").order_by("date", "created_at"):
        expenses_by_date.setdefault(expense.date, []).append(expense)

    weeks = []
    for week in month_days:
        week_cells = []
        for day in week:
            day_expenses = expenses_by_date.get(day, [])
            week_cells.append(
                {
                    "date": day,
                    "in_month": day.month == month,
                    "is_today": day == today,
                    "expenses": day_expenses,
                    "expense_total": sum((expense.amount for expense in day_expenses), Decimal("0")),
                }
            )
        weeks.append(week_cells)

    return {
        "year": year,
        "month": month,
        "month_start": month_start,
        "month_label": f"{SPANISH_MONTHS[month - 1]} {year}",
        "weekday_labels": ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"],
        "weeks": weeks,
        "today": today,
        "expenses_by_date": expenses_by_date,
    }
