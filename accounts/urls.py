from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomLoginForm

urlpatterns = [
   # post views
   # path('login/', views.user_login, name='login'),
   path('login/', auth_views.LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   path('register/', views.register, name='register'),
   path('register_receptionist/', views.register_receptionist, name='register_receptionist'),
   path('receptionist_saved/', views.receptionist_saved, name='receptionist_saved'),
   path('profile/', views.profile, name='profile'),
   path('upload_profile/', views.upload_profile, name='upload_profile'),
   

]