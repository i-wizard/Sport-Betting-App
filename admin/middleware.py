from django.http import HttpResponseRedirect


class AdminCheckMiddleware(object):
    def process_request(self, request):
        if request.user.is_authenticated:
            if not request.user.is_staff:
                return HttpResponseRedirect('/')
            else:
                return None
        else:
            return HttpResponseRedirect('/')
