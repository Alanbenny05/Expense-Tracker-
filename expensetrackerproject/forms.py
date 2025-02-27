from django import forms
from expensetrackerapp.models import Expense
  # Ensure this model exists

class RecurringExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'recurring', 'recurrence_period']

