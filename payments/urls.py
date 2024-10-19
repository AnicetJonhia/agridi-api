from django.urls import path
from .views import  PaymentCallbackView

urlpatterns = [

    path('callback/', PaymentCallbackView.as_view(), name='payment_callback'),
]
