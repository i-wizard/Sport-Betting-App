from django.urls import path

from admin.middleware import AdminCheckMiddleware
from .views import index_view, QuestionView, QuestionApiView, entries_view, entry_view
from utilities.general_middleware import AuthCheckLoginMiddleware
from django.utils.decorators import decorator_from_middleware

user_auth_decorator = decorator_from_middleware(AuthCheckLoginMiddleware)
admin_auth_decorator = decorator_from_middleware(AdminCheckMiddleware)
app_name = 'trivia'

urlpatterns = [
    path('', index_view, name='index'),
    path('question/<int:pk>', user_auth_decorator(QuestionView.as_view()), name='question'),
    path('entries', user_auth_decorator(entries_view), name='entries'),
    path('entries/<int:pk>', user_auth_decorator(entry_view), name='entry'),
    path('api/create-match', admin_auth_decorator(QuestionApiView.as_view())),
]
