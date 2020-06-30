from django.urls import path
from support.views import CreateProb, Issue, RespondIssue

app_name = 'support'
urlpatterns = [
    path('create', CreateProb.as_view(), name='create'),
    path('', Issue.as_view(), name='index'),
    path('respond', RespondIssue.as_view()),
]