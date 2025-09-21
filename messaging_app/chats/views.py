from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404
from .models import User, Conversation, Message
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer


# --------------------
# Conversation ViewSet
# --------------------


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all().prefetch_related("participants", "messages")
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["participants__email"]

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with participants.
        Expected JSON:
        {
            "participants": [
                "user_id1",
                "user_id2",
                ...
            ]
        }
        """
        participant_ids = request.data.get("participants", [])
        if len(participant_ids) < 2:
            return Response(
                {"error": "A conversation must have atleast 2 participants."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        participants = User.objects.filter(user_id__in=participant_ids)
        if participants.count() != len(participant_ids):
            return Response(
                {"error": "One or more participants do not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ---------------------
# Message ViewSet
# ---------------------


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all().select_related("sender", "conversation")
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["message_body"]

    def create(self, request, *args, **kwargs):
        """
        Send a new message in a conversation.
        Expected JSON:
        {
            "conversation": "conversation_id",
            "message_body": "",
            "sender": "user_id"
        }
        """
        conversation_id = request.data.get.get("conversation")
        sender_id = request.data.get("sender")
        message_body = request.data.get("message_body")

        if not conversation_id or not sender_id or not message_body:
            return Response(
                {"error": "conversation, sender, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        message = Message.objects.create(
            conversation_id=conversation_id,
            sender_id=sender_id,
            message_body=message_body,
        )
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)