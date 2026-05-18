from django.contrib import admin
from .models import Expense, Budget, SavingGoal

# Register your models here.

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["title", "amount", "category", "date", "user"]
    list_filter = ["category", "date"]
    search_fields = ["title", "description", "user__username"]
    list_per_page = 25

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ["user", "monthly_budget", "updated_at"]
    search_fields = ["user__username"]
    list_per_page = 25

@admin.register(SavingGoal)
class SavingGoalAdmin(admin.ModelAdmin):
    list_display = ["emoji", "title", "target_amount", "saved_amount", "user", "deadline"]
    list_filter = ["deadline", "created_at"]
    search_fields = ["title", "user__username"]
    list_per_page = 25