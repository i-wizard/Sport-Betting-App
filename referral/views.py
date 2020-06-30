from django.shortcuts import render

from referral.models import Referral


def referral_details(request):
    referrals = Referral.objects.filter(referrer=request.user.pk)
    return render(request, 'referral.html', {'referrals': referrals})
