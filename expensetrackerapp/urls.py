from django.urls import path
from . import views
from django.contrib.auth import views as auth_views 
from .views import CustomLoginView 
from .views import dashboard
from .views import profile

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
    path('profile/', profile, name='profile'),
]
