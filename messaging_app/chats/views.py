from rest_framework import viewsets, mixins, status, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer, UserSerializer
from django.db import models

class ConversationViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """
    A ViewSet for managing conversations.

    - list: Retrieve a list of all conversations for the authenticated user.
    - retrieve: Retrieve a single conversation by its ID.
    - create: Create a new conversation.
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns conversations where the authenticated user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user).order_by('-created_at')

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with multiple participants.
        """
        participants_data = request.data.get('participants')

        if not isinstance(participants_data, list) or len(participants_data) < 1:
            return Response({'error': 'A list of at least one participant ID is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            participants = [request.user]
            for user_id in participants_data:
                user = User.objects.get(pk=user_id)
                participants.append(user)
        except User.DoesNotExist:
            return Response({'error': 'One or more participant IDs were not found.'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Check for existing conversation with the same participants
        # This is a simplified check for exact participant matches
        existing_conversation = Conversation.objects.filter(participants__in=participants) \
                                                    .annotate(p_count=models.Count('participants')) \
                                                    .filter(p_count=len(participants)) \
                                                    .first()
        if existing_conversation:
            return Response(ConversationSerializer(existing_conversation).data, status=status.HTTP_200_OK)

        new_conversation = Conversation.objects.create()
        new_conversation.participants.set(participants)
        serializer = ConversationSerializer(new_conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    """
    A ViewSet for managing messages within a conversation.

    - list: Retrieve a list of messages for a specific conversation.
    - create: Send a new message to a conversation.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Returns messages for a specific conversation, ordered by creation time.
        """
        conversation_id = self.kwargs['conversation_pk']
        return Message.objects.filter(conversation_id=conversation_id).order_by('sent_at')

    def perform_create(self, serializer):
        """
        Set the sender and conversation for the message before saving.
        """
        conversation_id = self.kwargs['conversation_pk']
        conversation = get_object_or_404(Conversation, pk=conversation_id)
        # Check if the user is a participant in the conversation
        if self.request.user not in conversation.participants.all():
            raise serializers.ValidationError("You are not a participant in this conversation.")

        serializer.save(sender=self.request.user, conversation=conversation)
