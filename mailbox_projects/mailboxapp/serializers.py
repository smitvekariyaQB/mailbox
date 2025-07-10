from rest_framework import serializers
from .models import SentEmail, ReceivedEmail


class SentEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentEmail
        fields = ['id', 'subject', 'body', 'from_email', 'to_email', 'sent_at']
        read_only_fields = ['id', 'from_email', 'sent_at']


class ReceivedEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceivedEmail
        fields = ['id', 'subject', 'body', 'from_email', 'to_email', 'received_at']
        read_only_fields = ['id', 'from_email', 'to_email', 'received_at']