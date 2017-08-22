import swapper
from django.contrib.auth import get_user_model
from rest_framework import generics, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import RadiusAccountingSerializer, RadiusPostAuthSerializer

RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")
User = get_user_model()


@api_view(['POST'])
def authorize(request):
    username = request.data.get('username')
    password = request.data.get('password')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None
    if user and user.check_password(password):
        return Response({'control:Auth-Type': 'Accept'}, status=200)
    return Response({'control:Auth-Type': 'Reject'}, status=401)


class PostAuthView(generics.CreateAPIView):
    serializer_class = RadiusPostAuthSerializer

    def post(self, request, *args, **kwargs):
        """
        Sets the response data to None in order to instruct
        FreeRADIUS to avoid processing the response body
        """
        response = self.create(request, *args, **kwargs)
        response.data = None
        return response


postauth = PostAuthView.as_view()


class AccountingView(generics.ListCreateAPIView, mixins.UpdateModelMixin):
    queryset = RadiusAccounting.objects.all()
    """
    This implements list, create and update semantic, as freeradius will use post method
    in both the latter cases
    whether to create the object or update an existing one, will depend whether an object
    with the same unique_id already exists or not
    """
    serializer_class = RadiusAccountingSerializer

    def get_object(self):
        try:
            queryset = RadiusAccounting.objects.all()
            return queryset.get(unique_id=self.request.data.get('unique_id'))
        except RadiusAccounting.MultipleObjectsReturned:
            return queryset.filter(unique_id=self.request.data.get('unique_id')).first()
        except RadiusAccounting.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        method = 'create' if self.get_object() is None else 'update'
        response = getattr(self, method)(request, *args, **kwargs)
        response.data = None
        return response


accounting = AccountingView.as_view()
