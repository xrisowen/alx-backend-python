from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConversationViewSet, MessageViewSet

# Create a router for the main conversation viewset.
router = DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

urlpatterns = [
    # Include the main router URLs for conversations.
    path('', include(router.urls)),

    # Nested URL for messages within a specific conversation.
    # This manually links the MessageViewSet to a URL that includes
    # the conversation_pk from the URL pattern.
    path('conversations/<uuid:conversation_pk>/messages/',
         MessageViewSet.as_view({'get': 'list', 'post': 'create'}),
         name='message-list'),
    path('conversations/<uuid:conversation_pk>/messages/<uuid:pk>/',
         MessageViewSet.as_view({'get': 'retrieve'}),
         name='message-detail'),
]
