import swapper
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django.views import View
from rest_framework.authtoken.models import Token

RadiusToken = swapper.load_model('django_freeradius', 'RadiusToken')


class RedirectCaptivePageView(View):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        """
        redirect user to captive page
        with the social auth token in the querystring
        (which will allow the captive page to send the token to freeradius)
        """
        if not request.GET.get('cp'):
            return HttpResponse(_('missing cp GET param'), status=400)
        self.authorize(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_redirect_url(request))

    def authorize(self, request, *args, **kwargs):
        """
        authorization logic
        raises PermissionDenied if user is not authorized
        """
        user = request.user
        if not user.is_authenticated or not user.socialaccount_set.exists():
            raise PermissionDenied()

    def get_redirect_url(self, request):
        """
        refreshes token and returns the captive page URL
        """
        cp = request.GET.get('cp')
        user = request.user
        Token.objects.filter(user=user).delete()
        RadiusToken.objects.filter(user=user).delete()
        token = Token.objects.create(user=user)
        rad_token = RadiusToken.objects.create(user=user)
        return '{0}?username={1}&token={2}&radius_user_token={3}'.format(cp,
                                                                         user.username,
                                                                         token.key,
                                                                         rad_token.key)


redirect_cp = RedirectCaptivePageView.as_view()
