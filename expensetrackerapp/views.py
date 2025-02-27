import csv
from reportlab.pdfgen import canvas
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.http import HttpResponse
from .models import Expense
from django.utils.timezone import now
from django.shortcuts import render, redirect, get_object_or_404
from .models import Expense
from .form import ExpenseForm
from django.contrib.auth.decorators import login_required
import datetime
from .forms import RecurringExpenseForm



class CustomLoginView(LoginView):
    template_name = 'users/login.html'

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists!')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already registered!')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Account created successfully! Please log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
    
    return render(request, 'users/signup.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials!')
    
    return render(request, 'users/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    expenses = Expense.objects.filter(user=request.user).order_by('-date')
    
    total_expense = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    category_wise_expense = expenses.values('category').annotate(total=sum('amount'))
    
    return render(request, 'users/dashboard.html', {
        'expenses': expenses,
        'total_expense': total_expense,
        'category_wise_expense': category_wise_expense,
    })

@login_required
def dashboard(request):
    return render(request,'expensetrackerapp/dashboard.html')



@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def export_expenses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Amount', 'Description'])

    expenses = Expense.objects.filter(user=request.user)
    for expense in expenses:
        writer.writerow([expense.date, expense.amount, expense.description])

    return response


@login_required
def export_expenses_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="expenses_{now().date()}.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 800, f"Expense Report for {request.user.username}")
    p.drawString(100, 780, "-------------------------------------")

    expenses = Expense.objects.filter(user=request.user)
    y = 760
    for expense in expenses:
        p.drawString(100, y, f"{expense.date} - {expense.amount} - {expense.description}")
        y -= 20

    p.showPage()
    p.save()
    return response

@login_required
def check_budget(request):
    user_profile = request.user.profile
    total_expenses = sum(exp.amount for exp in Expense.objects.filter(user=request.user))

    if total_expenses > user_profile.budget_limit:
        messages.warning(request, "⚠️ You have exceeded your budget limit!")

    return render(request, 'expenses/dashboard.html', {'total_expenses': total_expenses})

def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "Expense added successfully!")
            return redirect('dashboard')
    else:
        form = ExpenseForm()
    return render(request, 'users/add_expense.html', {'form': form})

@login_required
def edit_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense updated successfully!")
            return redirect('dashboard')
    else:
        form = ExpenseForm(instance=expense)
    return render(request, 'users/edit_expense.html', {'form': form, 'expense': expense})

@login_required
def delete_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    messages.success(request, "Expense deleted successfully!")
    return redirect('dashboard')

@login_required
def expense_chart(request):
    today = datetime.date.today()
    start_of_month = today.replace(day=1)

    expenses = (
        Expense.objects.filter(user=request.user, date__gte=start_of_month)
        .values("date")
        .annotate(total=Sum("amount"))
        .order_by("date")
    )

    dates = [exp["date"].strftime("%Y-%m-%d") for exp in expenses]
    amounts = [exp["total"] for exp in expenses]

    return render(request, "expenses/chart.html", {"dates": dates, "amounts": amounts})

def some_view(request):
    return render(request, 'your_template.html')