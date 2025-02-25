from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
from .views import CustomLoginView 
from .views import dashboard

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]


urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
urlpatterns = [
    path('users/login/', CustomLoginView.as_view(), name='custom_login'),
]
urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
]
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('edit_expense/<int:expense_id>/', views.edit_expense, name='edit_expense'),
    path('delete_expense/<int:expense_id>/', views.delete_expense, name='delete_expense'),
]


urlpatterns = [
    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name='password_reset_complete'),
]
