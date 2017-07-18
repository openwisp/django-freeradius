from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

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
