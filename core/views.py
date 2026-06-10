from decimal import Decimal
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CustomUserCreationForm, ExpenseForm, BudgetForm, SavingGoalForm, ExpenseReportFilterForm
from .models import Expense, Budget, SavingGoal
from .services import advance_recurring_expenses, ensure_recurring_defaults, build_report_filename, filter_expenses_for_report
from .services.calendar import build_month_calendar
from .services.exporters import build_pdf_report, build_xlsx_report


def _get_user_budget(user):
    """Helper function to get user's budget or None."""
    return Budget.objects.filter(user=user).first()


def _sync_recurring_expenses(user):
    return advance_recurring_expenses(user)


@login_required
def index(request):
    _sync_recurring_expenses(request.user)
    expenses = Expense.objects.filter(user=request.user)
    month_start = timezone.localdate().replace(day=1)
    today = timezone.localdate()

    total_expenses = expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    total_this_month = expenses.filter(date__gte=month_start).aggregate(total=Sum("amount"))["total"] or Decimal("0.00")
    latest_expenses = expenses[:5]
    
    # Get or create budget for user
    budget = Budget.objects.filter(user=request.user).first()
    monthly_budget = budget.monthly_budget if budget else None
    remaining_budget = None
    budget_percentage = 0
    
    if monthly_budget:
        remaining_budget = monthly_budget - total_this_month
        budget_percentage = min(int((total_this_month / monthly_budget * 100)), 100) if monthly_budget > 0 else 0

    # Get saving goals for user
    saving_goals = SavingGoal.objects.filter(user=request.user)
    upcoming_fixed_expenses = expenses.filter(date__gte=today).order_by("date")[:5]
    upcoming_recurring_templates = expenses.filter(
        is_recurring=True,
        next_occurrence__isnull=False,
        next_occurrence__gte=today,
    ).order_by("next_occurrence")[:5]

    data = {
        "total_expenses": total_expenses,
        "total_this_month": total_this_month,
        "expense_count": expenses.count(),
        "latest_expenses": latest_expenses,
        "monthly_budget": monthly_budget,
        "remaining_budget": remaining_budget,
        "budget_percentage": budget_percentage,
        "budget": budget,
        "saving_goals": saving_goals,
        "upcoming_fixed_expenses": upcoming_fixed_expenses,
        "upcoming_recurring_templates": upcoming_recurring_templates,
    }
    return render(request, "core/index.html", data)


@login_required
def charts(request):
    _sync_recurring_expenses(request.user)
    expenses = Expense.objects.filter(user=request.user)
    month_start = timezone.localdate().replace(day=1)

    data = {
        "total_expenses": expenses.aggregate(total=Sum("amount"))["total"] or Decimal("0.00"),
        "total_this_month": expenses.filter(date__gte=month_start).aggregate(total=Sum("amount"))["total"] or Decimal("0.00"),
        "expense_count": expenses.count(),
    }
    return render(request, "core/charts.html", data)

def custom_logout(request):
    """Handle user logout and redirect to login page."""
    logout(request)
    return redirect("login")


def register(request):
    """Handle user registration."""
    data = {"form": CustomUserCreationForm()}

    if request.method == "POST":
        formulario = CustomUserCreationForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            usuario = authenticate(
                username=formulario.cleaned_data["username"],
                password=formulario.cleaned_data["password1"],
            )
            login(request, usuario)
            return redirect(to="dashboard")
        data["form"] = formulario

    return render(request, "registration/register.html", data)


def home(request):
    """Landing page for non-authenticated users"""
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "core/home.html")


@login_required
def expense_list(request):
    """Display list of user's expenses with filtering options."""
    _sync_recurring_expenses(request.user)
    expenses = Expense.objects.filter(user=request.user)
    
    # Filter by category
    category = request.GET.get('category')
    if category and category != '':
        expenses = expenses.filter(category=category)
    
    # Filter by month/year (format: YYYY-MM)
    month = request.GET.get('month')
    if month and month != '':
        try:
            year, month_num = month.split('-')
            expenses = expenses.filter(date__year=int(year), date__month=int(month_num))
        except (ValueError, AttributeError):
            pass
    
    # Search by title or description
    search = request.GET.get('search')
    if search and search != '':
        expenses = expenses.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )
    
    context = {
        "expenses": expenses,
        "categories": Expense.CATEGORY_CHOICES,
        "selected_category": category or '',
        "selected_month": month or '',
        "search_query": search or '',
        "report_form": ExpenseReportFilterForm(initial={"scope": "filtered", "category": category or ''}),
    }
    return render(request, "core/expenses/expense_list.html", context)


@login_required
def expense_detail(request, expense_id):
    """Display details of a specific expense."""
    _sync_recurring_expenses(request.user)
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    return render(request, "core/expenses/expense_detail.html", {"expense": expense})


@login_required
def expense_create(request):
    """Create a new expense."""
    form = ExpenseForm(request.POST or None)
    budget = _get_user_budget(request.user)
    
    if request.method == "POST" and form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        ensure_recurring_defaults(expense)
        expense.save()
        messages.success(request, "Gasto creado correctamente.")
        return redirect("expense_list")
    
    return render(
        request,
        "core/expenses/expense_form.html",
        {
            "form": form,
            "page_title": "Create Expense",
            "monthly_budget": budget.monthly_budget if budget else None,
        },
    )


@login_required
def expense_update(request, expense_id):
    """Update an existing expense."""
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)
    budget = _get_user_budget(request.user)
    
    if request.method == "POST" and form.is_valid():
        updated_expense = form.save(commit=False)
        ensure_recurring_defaults(updated_expense)
        updated_expense.save()
        messages.success(request, "Gasto actualizado correctamente.")
        return redirect("expense_list")
    
    return render(
        request,
        "core/expenses/expense_form.html",
        {
            "form": form,
            "page_title": "Edit Expense",
            "monthly_budget": budget.monthly_budget if budget else None,
        },
    )


@login_required
def expense_delete(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == "POST":
        expense.delete()
        messages.success(request, "Gasto eliminado correctamente.")
        return redirect("expense_list")
    return render(request, "core/expenses/expense_confirm_delete.html", {"expense": expense})


@login_required
def expense_calendar(request):
    _sync_recurring_expenses(request.user)
    current_date = timezone.localdate()
    year = request.GET.get("year")
    month = request.GET.get("month")
    category = request.GET.get("category") or ""

    try:
        year = int(year) if year else current_date.year
        month = int(month) if month else current_date.month
    except ValueError:
        year = current_date.year
        month = current_date.month

    calendar_data = build_month_calendar(request.user, year=year, month=month, category=category or None)
    month_start = calendar_data["month_start"]
    previous_month = month_start.replace(day=1) - timedelta(days=1)
    next_month = month_start.replace(day=28) + timedelta(days=4)
    next_month = next_month.replace(day=1)

    return render(
        request,
        "core/expenses/expense_calendar.html",
        {
            **calendar_data,
            "categories": Expense.CATEGORY_CHOICES,
            "selected_category": category,
            "selected_category_label": dict(Expense.CATEGORY_CHOICES).get(category, "Todas las categorías"),
            "previous_month": previous_month,
            "next_month": next_month,
        },
    )


@login_required
def export_expenses_pdf(request):
    _sync_recurring_expenses(request.user)
    form = ExpenseReportFilterForm(request.GET or None)
    form.is_valid()
    expenses = filter_expenses_for_report(request.user, form.cleaned_data if form.is_valid() else {})
    pdf_bytes = build_pdf_report(request.user, expenses)
    filename = build_report_filename(request.user, "pdf")
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@login_required
def export_expenses_xlsx(request):
    _sync_recurring_expenses(request.user)
    form = ExpenseReportFilterForm(request.GET or None)
    form.is_valid()
    expenses = filter_expenses_for_report(request.user, form.cleaned_data if form.is_valid() else {})
    xlsx_bytes = build_xlsx_report(request.user, expenses)
    filename = build_report_filename(request.user, "xlsx")
    response = HttpResponse(
        xlsx_bytes,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


# API endpoints for charts
@login_required
def api_expenses_by_category(request):
    """Return JSON data for pie chart: expenses by category"""
    expenses = Expense.objects.filter(user=request.user)
    
    category_data = {}
    for cat_key, cat_label in Expense.CATEGORY_CHOICES:
        total = expenses.filter(category=cat_key).aggregate(total=Sum("amount"))["total"] or 0
        category_data[cat_label] = float(total)
    
    # Filter out zero values for cleaner chart
    filtered_data = {k: v for k, v in category_data.items() if v > 0}
    
    return JsonResponse({
        "labels": list(filtered_data.keys()),
        "data": list(filtered_data.values()),
    })


@login_required
def api_expenses_by_month(request):
    """Return JSON data for bar chart: expenses by month (last 12 months)."""
    from datetime import timedelta
    
    expenses = Expense.objects.filter(user=request.user)
    today = timezone.localdate()
    monthly_data = {}
    
    # Calculate data for each month in the last 12 months
    for i in range(11, -1, -1):
        year = today.year
        month = today.month - (11 - i)
        
        if month <= 0:
            month += 12
            year -= 1
        
        month_date = today.replace(year=year, month=month, day=1)
        month_label = month_date.strftime('%b %Y')
        
        total = expenses.filter(
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(total=Sum("amount"))["total"] or 0
        
        monthly_data[month_label] = float(total)
    
    return JsonResponse({
        "labels": list(monthly_data.keys()),
        "data": list(monthly_data.values()),
    })


# Budget views
@login_required
def budget_edit(request):
    """View to edit user's monthly budget"""
    budget, created = Budget.objects.get_or_create(user=request.user)
    
    form = BudgetForm(request.POST or None, instance=budget)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Presupuesto actualizado correctamente.")
        return redirect("dashboard")
    
    return render(request, "core/budget_form.html", {"form": form, "budget": budget})


# Saving Goals views
@login_required
def saving_goals_list(request):
    """View to list all saving goals for the user"""
    goals = SavingGoal.objects.filter(user=request.user)
    return render(request, "core/saving_goals/goals_list.html", {"goals": goals})


@login_required
def saving_goal_create(request):
    """View to create a new saving goal"""
    form = SavingGoalForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        goal = form.save(commit=False)
        goal.user = request.user
        goal.save()
        messages.success(request, "Meta de ahorro creada correctamente.")
        return redirect("dashboard")
    
    return render(request, "core/saving_goals/goal_form.html", {"form": form, "page_title": "Crear Meta de Ahorro"})


@login_required
def saving_goal_edit(request, pk):
    """View to edit a saving goal"""
    goal = get_object_or_404(SavingGoal, pk=pk, user=request.user)
    form = SavingGoalForm(request.POST or None, instance=goal)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Meta de ahorro actualizada correctamente.")
        return redirect("dashboard")
    
    return render(request, "core/saving_goals/goal_form.html", {"form": form, "page_title": "Editar Meta de Ahorro", "goal": goal})


@login_required
def saving_goal_delete(request, pk):
    """View to delete a saving goal"""
    goal = get_object_or_404(SavingGoal, pk=pk, user=request.user)
    if request.method == "POST":
        goal.delete()
        messages.success(request, "Meta de ahorro eliminada correctamente.")
        return redirect("dashboard")
    
    return render(request, "core/saving_goals/goal_confirm_delete.html", {"goal": goal})
