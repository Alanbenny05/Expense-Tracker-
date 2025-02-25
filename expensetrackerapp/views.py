from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db.models import Sum
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required


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