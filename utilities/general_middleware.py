from django.http import HttpResponseRedirect


class AuthCheckMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return None
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect('/')


class AuthCheckLoginMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return None
            return HttpResponseRedirect('/admin')
        else:
            return HttpResponseRedirect('/login')


class ButAdminMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated:
            if request.user.is_staff:
                return HttpResponseRedirect('/admin')
        return None
