from django.http import HttpResponse
import csv
from django.utils.timezone import now, timedelta


def export_expenses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Amount'])

    # Example data (replace this with actual database query)
    expenses = [
        ['2024-02-26', 'Food', '100'],
        ['2024-02-25', 'Transport', '50'],
    ]

    for expense in expenses:
        writer.writerow(expense)

    return response

def export_expenses_pdf(request):
    return HttpResponse("PDF export feature coming soon.")

def check_budget(request):
    return HttpResponse("Budget check feature coming soon.")

import logging
from django.utils.timezone import now
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from expensetrackerapp.models import RecurringExpense, Expense


logger = logging.getLogger(__name__)  # Set up logging

def process_recurring_expenses():
    today = now().date()
    
    # Fetch all recurring expenses due today or earlier
    recurring_expenses = RecurringExpense.objects.filter(next_due_date__lte=today)

    for exp in recurring_expenses:
        # Check if an expense was already recorded today
        if not Expense.objects.filter(user=exp.User, amount=exp.amount, description=exp.description, date=today).exists():
            Expense.objects.create(
                user=exp.User,
                amount=exp.amount,
                description=exp.description,
                date=today  # Ensure date field exists in Expense model
            )
            logger.info(f"Processed recurring expense: {exp.description} for {exp.User}")

        # Update next due date based on frequency
        if exp.frequency == "daily":
            exp.next_due_date += timedelta(days=1)
        elif exp.frequency == "weekly":
            exp.next_due_date += timedelta(weeks=1)
        elif exp.frequency == "monthly":
            exp.next_due_date += relativedelta(months=1)

        exp.save()

    logger.info("Recurring expenses processing completed.")


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RecurringExpenseForm

@login_required
def recurring_expense_view(request):
    if request.method == "POST":
        form = RecurringExpenseForm(request.POST)
        if form.is_valid():
            recurring_expense = form.save(commit=False)
            recurring_expense.user = request.user
            recurring_expense.save()
            messages.success(request, "Recurring expense added successfully!")
            return redirect("dashboard")
        else:
            messages.error(request, "There was an error. Please check your input.")
    else:
        form = RecurringExpenseForm()

    return render(request, "expenses/recurring_expense.html", {"form": form})
