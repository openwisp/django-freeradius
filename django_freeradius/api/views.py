import drf_link_header_pagination
import swapper
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from django_freeradius.settings import API_TOKEN

from .serializers import RadiusAccountingSerializer, RadiusBatchSerializer, RadiusPostAuthSerializer

RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")
RadiusAccounting = swapper.load_model("django_freeradius", "RadiusAccounting")
User = get_user_model()
RadiusBatch = swapper.load_model("django_freeradius", "RadiusBatch")


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if request.META.get('HTTP_AUTHORIZATION', False):
            headers = request.META.get('HTTP_AUTHORIZATION').split(',')
            for header in headers:
                token = header.split(' ')[1]
                if token == API_TOKEN:
                    return (AnonymousUser(), None)
        if request.GET.get('token') == API_TOKEN:
            return (AnonymousUser(), None)
        raise AuthenticationFailed('Token authentication failed')


class AuthorizeView(APIView):
    authentication_classes = (TokenAuthentication, )

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username=username, is_active=True)
        except User.DoesNotExist:
            user = None
        if user and user.check_password(password):
            return Response({'control:Auth-Type': 'Accept'}, status=200)
        return Response({'control:Auth-Type': 'Reject'}, status=401)


authorize = AuthorizeView.as_view()


class PostAuthView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication, )
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


class AccountingFilter(filters.FilterSet):
    start_time = filters.DateTimeFilter(name='start_time', lookup_expr='gte')
    stop_time = filters.DateTimeFilter(name='stop_time', lookup_expr='gte')
    is_open = filters.BooleanFilter(method='filter_open')

    def filter_open(self, queryset, name,  value):
        if value:
            return queryset.filter(stop_time__isnull=True)
        return queryset.filter(stop_time__isnull=False)

    class Meta:
        model = RadiusAccounting
        fields = ('username',
                  'called_station_id',
                  'calling_station_id',
                  'start_time',
                  'stop_time',
                  'is_open')


class AccountingViewPagination(drf_link_header_pagination.LinkHeaderPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AccountingView(generics.ListCreateAPIView):
    """
    HEADER: Pagination is provided using a Link header
            https://developer.github.com/v3/guides/traversing-with-pagination/

    GET: get list of accounting objects

    POST: add or update accounting information (start, interim-update, stop);
          does not return any JSON response so that freeradius will avoid
          processing the response without generating warnings
    """
    authentication_classes = (TokenAuthentication, )
    queryset = RadiusAccounting.objects.all()
    serializer_class = RadiusAccountingSerializer
    pagination_class = AccountingViewPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = AccountingFilter

    def post(self, request, *args, **kwargs):
        status_type = self._get_status_type(request)
        # Accounting-On and Accounting-Off are not implemented and
        # hence  ignored right now - may be implemented in the future
        if status_type in ['Accounting-On', 'Accounting-Off']:
            return Response(None)
        method = 'create' if status_type == 'Start' else 'update'
        return getattr(self, method)(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        is_start = request.data['status_type'] == 'Start'
        for field in ['session_time', 'input_octets', 'output_octets']:
            if is_start and request.data[field] == '':
                request.data[field] = 0
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid()
        error_keys = serializer.errors.keys()
        errors = len(error_keys)
        if not errors:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(None, status=201, headers=headers)
        # trying to create a record which
        # already exist, fallback to update
        if errors == 1 and 'unique_id' in error_keys:
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(serializer.errors)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_queryset().get(unique_id=request.data['unique_id'])
        # trying to update a record which
        # does not exist, fallback to create
        except RadiusAccounting.DoesNotExist:
            return self.create(request, *args, **kwargs)
        serializer = self.get_serializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(None)

    def _get_status_type(self, request):
        try:
            return request.data['status_type']
        except KeyError:
            raise ValidationError({'status_type': [_('This field is required.')]})


accounting = AccountingView.as_view()


class BatchView(generics.CreateAPIView):
    queryset = RadiusBatch.objects.all()
    serializer_class = RadiusBatchSerializer

    def post(self, request, *args, **kwargs):
        serializer = RadiusBatchSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            expiration_date = serializer.data.get('expiration_data')
            strategy = serializer.data.get('strategy')
            if strategy == 'csv':
                csvfile = request.FILES['csvfile']
                batch = RadiusBatch(name=name,
                                    strategy=strategy,
                                    expiration_date=expiration_date,
                                    csvfile=csvfile)
                batch.csvfile_upload(csvfile)
                response = RadiusBatchSerializer(batch)
                return Response(response.data, status=status.HTTP_201_CREATED)
            elif strategy == 'prefix':
                prefix = serializer.data.get('prefix')
                batch = RadiusBatch(name=name,
                                    strategy=strategy,
                                    expiration_date=expiration_date,
                                    prefix=prefix)
                number_of_users = int(request.data['number_of_users'])
                number_of_users_validated = self._validate_number_of_users(number_of_users)
                batch.prefix_add(prefix, number_of_users_validated)
                response = RadiusBatchSerializer(batch)
                return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _validate_number_of_users(self, number):
        if number > 0:
            return number
        else:
            raise ValidationError({'number_of_users': [_('Number of users should be greater than 0.')]})


batch = BatchView.as_view()
