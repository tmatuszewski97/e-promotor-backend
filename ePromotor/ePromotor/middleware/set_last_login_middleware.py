from django.utils.deprecation import MiddlewareMixin
from django.utils.timezone import now
from core.models import User


class SetLastLoginMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            # Update last_login time after request was finished
            User.objects.filter(pk=request.user.pk).update(last_login=now())
        return response
