from django.urls import path
from .views import (
    api_expenses_by_category,
    api_expenses_by_month,
    budget_edit,
    charts,
    custom_logout,
    expense_calendar,
    expense_create,
    expense_delete,
    expense_detail,
    expense_list,
    expense_update,
    export_expenses_pdf,
    export_expenses_xlsx,
    home,
    index,
    register,
    saving_goal_create,
    saving_goal_delete,
    saving_goal_edit,
    saving_goals_list,
)



# Urls pagina

urlpatterns = [
    path('', home, name="home"),
    path('dashboard/', index, name="dashboard"),
    path('charts/', charts, name="charts"),
    path('calendar/', expense_calendar, name="expense_calendar"),

    path('expenses/', expense_list, name="expense_list"),
    path('expenses/add/', expense_create, name="expense_create"),
    path('expenses/<int:expense_id>/', expense_detail, name="expense_detail"),
    path('expenses/<int:expense_id>/edit/', expense_update, name="expense_update"),
    path('expenses/<int:expense_id>/delete/', expense_delete, name="expense_delete"),
    path('reports/export/pdf/', export_expenses_pdf, name="export_expenses_pdf"),
    path('reports/export/xlsx/', export_expenses_xlsx, name="export_expenses_xlsx"),

    path('register/', register, name="register"),
    path('accounts/logout/', custom_logout, name='logout'),
    
    # API endpoints for charts
    path('api/expenses-by-category/', api_expenses_by_category, name="api_expenses_by_category"),
    path('api/expenses-by-month/', api_expenses_by_month, name="api_expenses_by_month"),
    
    # Budget
    path('budget/edit/', budget_edit, name="budget_edit"),
    
    # Saving Goals
    path('saving-goals/', saving_goals_list, name="saving_goals_list"),
    path('saving-goals/add/', saving_goal_create, name="saving_goal_create"),
    path('saving-goals/<int:pk>/edit/', saving_goal_edit, name="saving_goal_edit"),
    path('saving-goals/<int:pk>/delete/', saving_goal_delete, name="saving_goal_delete"),
]