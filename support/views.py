from django.contrib import messages
from django.shortcuts import render
from django.views.generic.base import View
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from stack.stackSerializers import IssueResponseSerializer
from support.forms import IssueForm
from support.models import Support
from support.supportSerializers import SupportSerializer
from utilities.helper import LargeResultsSetPagination, Helper, Mailer

helpers = Helper()


def support_view(request):
    return render(request, 'support.html')


class CreateProb(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = SupportSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(data={'response': 'Issue reported you will be notified as soon as possible.'},
                        status=status.HTTP_200_OK)


class Issue(View):
    form = IssueForm

    def get(self, request):
        self.form = self.form()

        return render(request, 'support.html', {'form': self.form})

    def post(self, request):
        form = self.form(request.POST)

        if form.is_valid():
            form.save()
            mailer = Mailer()
            mailer.send_support_message(form.cleaned_data['username'])
            messages.success(request, 'Message Received! We\'ll get back to you as soon as possible.')

        return render(request, 'support.html', {'form': form})


class CreatedIssues(generics.ListAPIView):
    queryset = Support.objects.all()
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = SupportSerializer
    pagination_class = LargeResultsSetPagination


class RespondIssue(APIView):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = IssueResponseSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        helpers.admin_send_mail(message_body=request.data.get('message'), subject=request.data.get('title'),
                                email=request.data.get('email'))

        return Response(data={'response': 'Response sent!'},
                        status=status.HTTP_200_OK)
