from .views import LoginView, LogoutView
from django.urls import path, include

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='log_out'),
    
]
