from django.urls import path

from .views import DashBoardView, LectureListView, LectureView, NewLectureView, QREnd, QRStart

urlpatterns = [
    path('', DashBoardView.as_view(), name='dashboard'),
    path('lecture/<int:pk>', LectureView.as_view(), name='lecture'),
    path('lecture/<int:pk>/qr_start', QRStart.as_view(), name='qr_start'),
    path('lecture/<int:pk>/qr_end', QREnd.as_view(), name='qr_end'),
    path('lecture/new', NewLectureView.as_view(), name='new_lecture'),
    path('lecture/all', LectureListView.as_view(), name='lectures_list'),
]
