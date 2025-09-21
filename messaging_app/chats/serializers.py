from rest_framework import serializers
from chats.models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['user_id', 'username', 'first_name', 'last_name', 'email', 'role']

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['message_id', 'sender', 'message_body', 'sent_at', 'conversation']
        read_only_fields = ['sent_at']
        extra_kwargs = {
            'conversation': {'write_only': True}
        }

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Conversation model, including nested messages and participants.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'messages', 'created_at']
