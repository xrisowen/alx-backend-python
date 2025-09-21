"""
Data models for the API application.

Models are structured to demonstrate relationships as requested in the overview.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser):
    """
    Custom User model to allow for future expansion.
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # The default Django User model already handles first_name, last_name,
    # email (inherited from AbstractUser).
    # The 'unique=True' constraint automatically adds an index.
    # The 'db_index=True' is added here to explicitly follow the schema.
    email = models.EmailField(unique=True, db_index=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    
    # ENUM for role, represented using choices
    class Role(models.TextChoices):
        GUEST = 'guest', 'Guest'
        HOST = 'host', 'Host'
        ADMIN = 'admin', 'Admin'

    role = models.CharField(
        max_length=5,
        choices=Role.choices,
        default=Role.GUEST,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Property(models.Model):
    """
    A model to represent a property listing.
    """
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # One-to-many relationship with User
    # Django automatically indexes ForeignKeys, but db_index is added for clarity based on schema.
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', db_index=True)

    def __str__(self):
        return self.title

class Booking(models.Model):
    """
    A model to represent a booking for a property.
    """
    start_date = models.DateField()
    end_date = models.DateField()
    # One-to-many relationship with User (the guest)
    # db_index=True is added for clarity based on schema.
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', db_index=True)
    # One-to-many relationship with Property
    # db_index=True is added for clarity based on schema.
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='bookings', db_index=True)

    class Meta:
        # Example of a custom index on multiple fields for performance on common queries
        # The 'property_id' and 'booking_id' indexes from the schema are implicitly
        # handled by the ForeignKeys, but this shows how to add a custom index.
        indexes = [
            models.Index(fields=['start_date', 'end_date']),
        ]

    def __str__(self):
        return f'Booking for {self.property.title} by {self.guest.username}'

class Conversation(models.Model):
    """
    A model to represent a conversation between users.
    """
    conversation_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Many-to-many relationship with User
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        participant_names = ", ".join([user.username for user in self.participants.all()])
        return f'Conversation with {participant_names}'

class Message(models.Model):
    """
    A model to represent a message within a conversation.
    """
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # One-to-many relationship with User (the sender)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    # One-to-many relationship with Conversation
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    message_body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender.username} in conversation {self.conversation.conversation_id}'
