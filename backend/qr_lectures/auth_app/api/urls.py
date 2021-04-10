from django.urls import path

from .views import GetTokenView


urlpatterns = [
    path('get_token/', GetTokenView.as_view(), name='get_token'),
    
]
