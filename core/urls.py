from django.urls import path
from .views import SliderView, AdminSliderView

urlpatterns = [
    path('user-slider', SliderView.as_view(), name='user_slider_view'),
    path('admin-slider', AdminSliderView.as_view(), name='admin_slider_view'),
]
