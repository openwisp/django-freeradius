import logging

import drf_link_header_pagination
import swapper
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed, ParseError, ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .. import settings as app_settings
from .serializers import RadiusAccountingSerializer, RadiusBatchSerializer, RadiusPostAuthSerializer

RadiusPostAuth = swapper.load_model('django_freeradius', 'RadiusPostAuth')
RadiusAccounting = swapper.load_model('django_freeradius', 'RadiusAccounting')
User = get_user_model()
RadiusBatch = swapper.load_model('django_freeradius', 'RadiusBatch')
RadiusToken = swapper.load_model('django_freeradius', 'RadiusToken')

if app_settings.REST_USER_TOKEN_ENABLED:
    from rest_framework.authtoken.models import Token


class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        if request.META.get('HTTP_AUTHORIZATION', False):
            headers = request.META.get('HTTP_AUTHORIZATION').split(',')
            for header in headers:
                try:
                    token = header.split(' ')[1]
                except IndexError:
                    raise ParseError('Invalid token')
                if token == app_settings.API_TOKEN:
                    return (AnonymousUser(), None)
        if request.GET.get('token') == app_settings.API_TOKEN:
            return (AnonymousUser(), None)
        raise AuthenticationFailed('Token authentication failed')


class AuthorizeView(APIView):
    authentication_classes = (TokenAuthentication, )
    accept_attributes = {'control:Auth-Type': 'Accept'}
    accept_status = 200
    reject_attributes = {'control:Auth-Type': 'Reject'}
    reject_status = 401

    def post(self, request, *args, **kwargs):
        user = self.get_user(request)
        if user and self.authenticate_user(request, user):
            return Response(self.accept_attributes,
                            status=self.accept_status)
        if app_settings.API_AUTHORIZE_REJECT:
            return Response(self.reject_attributes,
                            status=self.reject_status)
        else:
            return Response(None, status=200)

    def get_user(self, request):
        """
        return active user or ``None``
        """
        try:
            return User.objects.get(username=request.data.get('username'),
                                    is_active=True)
        except User.DoesNotExist:
            return None

    def authenticate_user(self, request, user):
        """
        returns ``True`` if the password value supplied is
        a valid user password or a valid user token
        can be overridden to implement more complex checks
        """
        return user.check_password(request.data.get('password')) or \
               self.check_user_token(request, user)  # noqa

    def check_user_token(self, request, user):
        """
        returns ``True`` if the password value supplied is a valid
        radius user token
        """

        try:
            token = RadiusToken.objects.get(
                user=user,
                key=request.data.get('password')
            )
        except RadiusToken.DoesNotExist:
            token = None
        if app_settings.DISPOSABLE_RADIUS_USER_TOKEN and token is not None:
            token.delete()
        return token is not None


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
    start_time = filters.DateTimeFilter(field_name='start_time', lookup_expr='gte')
    stop_time = filters.DateTimeFilter(field_name='stop_time', lookup_expr='lte')
    is_open = filters.BooleanFilter(field_name='stop_time',
                                    lookup_expr='isnull',
                                    label='Is Open')

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
    queryset = RadiusAccounting.objects.all().order_by('-start_time')
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
        data = request.data.copy()  # import because request objects is immutable
        for field in ['session_time', 'input_octets', 'output_octets']:
            if is_start and request.data[field] == '':
                data[field] = 0
        serializer = self.get_serializer(data=data)
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

    def perform_create(self, serializer):
        if app_settings.API_ACCOUNTING_AUTO_GROUP:
            user_model = get_user_model()
            username = serializer.validated_data.get('username', '')
            try:
                user = user_model.objects.get(username=username)
            except User.DoesNotExist:
                logging.info('no corresponding user found '
                             'for username: {}'.format(username))
                serializer.save()
            else:
                group = user.radiususergroup_set.order_by('priority').first()
                # user may not have a group defined
                groupname = group.groupname if group else None
                serializer.save(groupname=groupname)
        else:
            return super().perform_create(serializer)

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
    authentication_classes = (TokenAuthentication, )
    queryset = RadiusBatch.objects.all()
    serializer_class = RadiusBatchSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.data.get('name')
            expiration_date = serializer.data.get('expiration_data')
            strategy = serializer.data.get('strategy')
            if strategy == 'csv':
                csvfile = request.FILES['csvfile']
                options = dict(name=name, strategy=strategy,
                               expiration_date=expiration_date,
                               csvfile=csvfile)
                batch = self._create_batch(serializer, **options)
                batch.csvfile_upload(csvfile)
                response = RadiusBatchSerializer(batch)
            elif strategy == 'prefix':
                prefix = serializer.data.get('prefix')
                options = dict(name=name, strategy=strategy,
                               expiration_date=expiration_date,
                               prefix=prefix)
                batch = self._create_batch(serializer, **options)
                number_of_users = int(request.data['number_of_users'])
                batch.prefix_add(prefix, number_of_users)
                response = RadiusBatchSerializer(batch)
            return Response(response.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def _create_batch(self, serializer, **kwargs):
        batch = RadiusBatch(**kwargs)
        return batch


batch = BatchView.as_view()


if app_settings.REST_USER_TOKEN_ENABLED:
    from rest_framework.authtoken.serializers import AuthTokenSerializer
    from rest_framework.authtoken.views import ObtainAuthToken as BaseObtainAuthToken
    from rest_framework import serializers
    from django.views.decorators.csrf import csrf_exempt

    class TokenSerializer(serializers.ModelSerializer):
        class Meta:
            model = Token
            fields = ('key',)

    class RadiusTokenMixin(object):
        def get_or_create_radius_token(self, user):
            """
            Designed to be overridden by extensions
            """
            radius_token, rad_token_created = self.radius_token.objects.get_or_create(user=user)
            return radius_token

    class ObtainAuthTokenView(RadiusTokenMixin, BaseObtainAuthToken):
        serializer_class = TokenSerializer
        auth_serializer_class = AuthTokenSerializer
        authentication_classes = []
        radius_token = RadiusToken

        def get_user(self, serializer):
            """
            Designed to be overridden by extensions
            """
            return serializer.validated_data['user']

        def post(self, request, *args, **kwargs):
            serializer = self.auth_serializer_class(
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            user = self.get_user(serializer, *args, **kwargs)
            token, created = Token.objects.get_or_create(user=user)
            radius_token = self.get_or_create_radius_token(user)
            context = {'view': self,
                       'request': request,
                       'token_login': True}
            serializer = self.serializer_class(instance=token,
                                               context=context)
            response = {'radius_user_token': radius_token.key}
            response.update(serializer.data)
            return Response(response)

    obtain_auth_token = csrf_exempt(ObtainAuthTokenView.as_view())

    class ValidateAuthTokenView(RadiusTokenMixin, generics.CreateAPIView):
        radius_token = RadiusToken

        def post(self, request, *args, **kwargs):
            request_token = request.data.get('token')
            response = {'response_code': 'BLANK_OR_INVALID_TOKEN'}
            if request_token:
                try:
                    token = Token.objects.get(key=request_token)
                    radius_token = self.get_or_create_radius_token(token.user)
                    response = {
                        'response_code': 'AUTH_TOKEN_VALIDATION_SUCCESSFUL',
                        'auth_token': token.key,
                        'radius_user_token': radius_token.key
                    }
                    return Response(response, 200)
                except Token.DoesNotExist:
                    pass
            return Response(response, 401)

    validate_auth_token = (ValidateAuthTokenView.as_view())
