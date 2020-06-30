from django.shortcuts import render


def faqs_view(request):
    return render(request, 'faqs.html')


def how_to_play(request):
    return render(request, 'how_to_play.html')
