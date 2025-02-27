from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from django import forms
from django.utils.timezone import now




# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True

class Category(TimeStampedModel):
    def __str__(self):
        return self.name
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=20)

class Budget(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit_amount = models.DecimalField(max_digits=10,decimal_places=2)

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    date = models.DateField(default=now)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

# #class Alert(TimeStampedModel):
#     user_id  = models.Foreignkey(User, on_delete=models.CASCADE)
#     alert_type = models.CharField(max_length=20)
#     related_budget_id = models.ForeignKey(Budget, on_delete=models.CASECADE)
#     message = models.CharField()
#     is_read = models.BooleanField()
   

class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transport', 'Transport'),
        ('Rent', 'Rent'),
        ('Entertainment', 'Entertainment'),
         ('bills', 'Bills'),
        ('Others', 'Others'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Untitled Expense")

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Others')
    recurring = models.BooleanField(default=False)
    recurrence_period = models.CharField(max_length=20, choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('monthly', 'Monthly')], blank=True, null=True)
    date = models.DateField(default=now)

    

   


def __str__(self):
        return f"{self.title} - {self.amount}"
    
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    


class RecurringExpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Renamed `User` to `user`
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    frequency = models.CharField(
        max_length=10,
        choices=[("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly")]
    )
    next_due_date = models.DateField(editable=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Track when it was added

    def update_next_due_date(self):
        """Update next_due_date based on frequency"""
        if self.frequency == "daily":
            self.next_due_date += timedelta(days=1)
        elif self.frequency == "weekly":
            self.next_due_date += timedelta(weeks=1)
        elif self.frequency == "monthly":
            self.next_due_date += timedelta(weeks=4)  # Approximate month handling
        self.save()

    def __str__(self):
        return f"{self.description} - {self.frequency} - Due: {self.next_due_date}"

class RecurringExpenseForm(forms.ModelForm):
    class Meta:
        model = RecurringExpense
        fields = ["amount", "description", "frequency"]  # Remove "next_due_date"

