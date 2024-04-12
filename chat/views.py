from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework import status
from rest_framework.decorators import action
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
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, url_path='search')
    def get_queryset(self, req):
        search_term = req.query_params.get('term', None)
        if search_term is None or search_term == '':
            users = User.objects.none()
        else:
            users = User.objects.filter(username__contains=search_term)

        page = self.paginate_queryset(users)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all().order_by('created')
    serializer_class = ChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, url_path="me")
    def user_chats(self, req):
        user = req.user
        user_chats = Chat.objects.filter(members__member_id=user.id)

        page = self.paginate_queryset(user_chats)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

    @action(detail=False, url_path="start")
    def start_chat(self, req):
        current_user = req.user
        user = req.query_params.get('user', None)
        chat = Chat.objects.filter(type='private', members__member_id__in=[current_user.id, user]).distinct().first()
        if not chat:
            chat = Chat(type='private')
            chat.save()
            chat_member_1 = ChatMember(chat_id=chat, member_id_id=current_user.id)
            chat_member_1.save()
            chat_member_2 = ChatMember(chat_id=chat, member_id_id=user)
            chat_member_2.save()
            chat.members.add(chat_member_1)
            chat.members.add(chat_member_2)

        serializer = self.get_serializer(chat, many=False)
        return Response(serializer.data)


class ChatMemberViewSet(viewsets.ModelViewSet):
    queryset = ChatMember.objects.all()
    serializer_class = ChatMemberSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().order_by('created')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, url_path="chat")
    def chat_messages(self, req):
        current_user = req.user
        chat_id = req.query_params.get('chat_id', None)
        is_user_chat_member = ChatMember.objects.filter(chat_id_id=chat_id, member_id_id=current_user.id).exists()
        if is_user_chat_member:
            messages = Message.objects.filter(chat_id__id=chat_id).order_by('created')
        else:
            messages = Message.objects.none()

        page = self.paginate_queryset(messages)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
