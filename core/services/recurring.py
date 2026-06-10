from calendar import monthrange
from datetime import date, timedelta

from django.utils import timezone

from ..models import Expense


def advance_recurring_date(current_date, frequency):
    if frequency == Expense.RECURRING_FREQUENCY_DAILY:
        return current_date + timedelta(days=1)
    if frequency == Expense.RECURRING_FREQUENCY_WEEKLY:
        return current_date + timedelta(weeks=1)
    if frequency == Expense.RECURRING_FREQUENCY_MONTHLY:
        year = current_date.year + (current_date.month // 12)
        month = current_date.month % 12 + 1
        last_day = monthrange(year, month)[1]
        return date(year, month, min(current_date.day, last_day))
    return None


def ensure_recurring_defaults(expense):
    if not expense.is_recurring:
        expense.recurrence_frequency = Expense.RECURRING_FREQUENCY_NONE
        expense.next_occurrence = None
        return expense

    if expense.recurrence_frequency and not expense.next_occurrence:
        next_occurrence = advance_recurring_date(expense.date, expense.recurrence_frequency)
        expense.next_occurrence = next_occurrence or expense.date

    return expense


def advance_recurring_expenses(user, as_of=None):
    today = as_of or timezone.localdate()
    templates = Expense.objects.filter(
        user=user,
        is_recurring=True,
    ).exclude(recurrence_frequency=Expense.RECURRING_FREQUENCY_NONE).order_by("date", "created_at")

    generated_count = 0

    for template in templates:
        next_due = template.next_occurrence or advance_recurring_date(template.date, template.recurrence_frequency)
        if not next_due:
            continue

        while next_due and next_due <= today:
            exists = Expense.objects.filter(
                user=user,
                recurrence_parent=template,
                date=next_due,
            ).exists()
            if not exists:
                Expense.objects.create(
                    user=user,
                    title=template.title,
                    amount=template.amount,
                    category=template.category,
                    date=next_due,
                    description=template.description,
                    is_recurring=False,
                    recurrence_frequency=Expense.RECURRING_FREQUENCY_NONE,
                    next_occurrence=None,
                    recurrence_parent=template,
                )
                generated_count += 1

            next_due = advance_recurring_date(next_due, template.recurrence_frequency)

        if template.next_occurrence != next_due:
            template.next_occurrence = next_due
            template.save(update_fields=["next_occurrence", "updated_at"])

    return generated_count
