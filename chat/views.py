from django.contrib.auth.models import Group, User
from django.shortcuts import render, redirect
from rest_framework import permissions, viewsets

from chat.models import Chat, ChatMember, Message
from chat.serializers import UserSerializer, GroupSerializer, ChatSerializer, ChatMemberSerializer, MessageSerializer


def chat_page(request, *args, **kwargs):
    if not request.user.is_authenticated:
        return redirect("login-user")
    context = {}
    return render(request, "chat/ChatPage.html", context)


# @csrf_exempt
# def chat_list(request, *args, **kwargs):
#     if request.method == 'GET':
#         chats = Chat.objects.all()
#         serializer = ChatSerializer(chats, many=True)
#         return JsonResponse(serializer.data, safe=False)
#     elif request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = ChatSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
#         return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#

# @csrf_exempt
# def chat_detail(request, pk, *args, **kwargs):
#     try:
#         chat = Chat.objects.get(pk=pk)
#     except Chat.DoesNotExist:
#         return JsonResponse({'error': 'Chat does not exist'}, status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = ChatSerializer(chat)
#         return JsonResponse(serializer.data)
#     elif request.method == 'DELETE':
#         chat.delete()
#         return JsonResponse({'error': 'Chat deleted successfully'}, status=status.HTTP_200_OK)


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
