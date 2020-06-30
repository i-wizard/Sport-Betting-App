from rest_framework import serializers

from .models import Slider


class UserSliderImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'


class SliderImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slider
        fields = '__all__'
