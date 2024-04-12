from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

from chat.models import Chat, ChatMember, Message
from chat.serializers import GroupSerializer, ChatSerializer, ChatMemberSerializer, MessageSerializer, \
    UserRegistrationSerializer
from .serializers import UserSerializer


class UserRegistrationView(APIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            access = AccessToken.for_user(user)
            refresh = RefreshToken.for_user(user)
            res = {
                'refresh': str(refresh),
                'access': str(access),
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all().order_by('created')
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChatMemberViewSet(viewsets.ModelViewSet):
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('created')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
