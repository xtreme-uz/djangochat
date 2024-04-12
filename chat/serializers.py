from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from rest_framework import serializers

from chat.models import Chat, ChatMember, Message


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']

        return User.objects.create_user(username=username, email=email, password=password)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'

    def create(self, validated_data):
        return Chat.objects.create(**validated_data)


class ChatMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMember
        fields = '__all__'

    def validate(self, data):
        chat_id = data.get('chat_id').id
        members_count = ChatMember.objects.filter(chat_id=chat_id).count()
        chat_type = Chat.objects.filter(id=chat_id).get().type

        if chat_type == 'private' and members_count >= 2:
            raise serializers.ValidationError("You can't join to a private chat")

        return data

    def create(self, validated_data):
        return ChatMember.objects.create(**validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

    def create(self, validated_data):
        return Message.objects.create(**validated_data)
