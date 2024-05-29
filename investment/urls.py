from django.urls import path
from .views import LoginView,RegistrationView,LogoutView,DashboardView


app_name = 'investment'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('dashboard/',DashboardView.as_view(),name="dashboard"),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    path('dashboard/delete/<int:investment_id>/', DashboardView.as_view(), name='delete_investment'),

]
