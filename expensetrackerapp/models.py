from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        abstract = True

class Category(TimeStampedModel):
    def __str__(self):
        return self.name
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    description = models.TextField()

class Budget(TimeStampedModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit_amount = models.DecimalField(max_digits=10,decimal_places=2)

# #class Alert(TimeStampedModel):
#     user_id  = models.Foreignkey(User, on_delete=models.CASCADE)
#     alert_type = models.CharField(max_length=20)
#     related_budget_id = models.ForeignKey(Budget, on_delete=models.CASECADE)
#     message = models.CharField()
#     is_read = models.BooleanField()
    

