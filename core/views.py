from django.shortcuts import render
from rest_framework import status, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from stack.models import Slip
from users.models import User
from utilities.helper import LargeResultsSetPagination
from .coreSerializers import UserSliderImageSerializers, SliderImageSerializer
from .models import Slider


def homepage(request):
    sliders = Slider.objects.all().filter(should_show=True).order_by('-id')
    num_bets = 0

    if request.user.is_authenticated:
        num_bets = Slip.objects.filter(game_fate=0, user=request.user.pk).count()

    ref = ''
    return render(request, 'homepage.html', {'sliders': sliders, 'ref': ref, 'num_bets': num_bets})


def ref_homepage(request, token):
    sliders = Slider.objects.all().filter(should_show=True).order_by('-id')

    ref = token
    if ref:
        try:
            User.objects.get(referral_code=ref)
        except User.DoesNotExist:
            ref = ''
    return render(request, 'homepage.html', {'sliders': sliders, 'ref': ref})


class SliderView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSliderImageSerializers

    def get(self, request):
        queryset = Slider.objects.all().filter(should_show=True).order_by('-id')

        serializer = self.serializer_class(queryset, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class AdminSliderView(generics.ListAPIView):
    permission_classes = (permissions.IsAdminUser,)
    queryset = Slider.objects.all().order_by('-id')
    serializer_class = SliderImageSerializer
    pagination_class = LargeResultsSetPagination

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data=True, status=status.HTTP_200_OK)

    def patch(self, request):
        queryset = Slider.objects.get(pk=request.data['image'])

        should_show = False
        if request.data.get('should_show') == 1:
            should_show = True
        queryset.should_show = should_show
        queryset.save(update_fields=('should_show',))

        return Response(data=True, status=status.HTTP_200_OK)


def privacy(request):
    return render(request, 'privacy.html')


def terms_condition_view(request):
    return render(request, 'terms.html')
