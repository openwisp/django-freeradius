import swapper
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.response import Response

RadiusPostAuth = swapper.load_model("django_freeradius", "RadiusPostAuth")

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


@api_view(['POST'])
def postauth(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')
        reply = request.data.get('reply')
        if reply == 'Access-Accept':
            password = ''
        RadiusPostAuth.objects.create(username=username, password=password, reply=reply)
        return Response({''}, status=204)
    except:  # pragma: no cover
        return Response({''}, status=500)
