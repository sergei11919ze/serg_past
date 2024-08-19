from django.urls import path
from .views import  IndexAPIView, index, create_pdf



urlpatterns = [
    path('api/v1/', IndexAPIView.as_view()),
    
    path('api/v1/pdf/<str:ip>/<str:id>/', create_pdf),
    path('api/v1/<str:pk>/', index),
    
]