from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



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
    date = models.DateField(auto_now_add=True)

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
        ('Others', 'Others'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="Untitled Expense")

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Others')
   

date = models.DateField(auto_now_add=True, default=timezone.now)

   


def __str__(self):
        return f"{self.title} - {self.amount}"
    
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    budget_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.user.username}'s Profile"