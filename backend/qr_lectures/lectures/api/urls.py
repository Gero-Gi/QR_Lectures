from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import LectureViewSet, SessionView

router = DefaultRouter()
router.register(r'lecture', LectureViewSet, basename='lectures_api')

# router.register(r'tax_rule', TaxRule, basename='tax_rule')

urlpatterns = [
    path('', include(router.urls)),
    path('session/<int:lecture_pk>', SessionView.as_view(), name='session_api'),
]