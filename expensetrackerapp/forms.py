from django import forms
from django.contrib.auth.models import User
from .models import Profile
from .models import RecurringExpense

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']

class RecurringExpenseForm(forms.ModelForm):
    class Meta:
        model = RecurringExpense
        fields = ["amount", "description", "frequency", "next_due_date"]


from .models import Expense

class RecurringExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['title', 'amount', 'category', 'recurring', 'recurrence_period']

