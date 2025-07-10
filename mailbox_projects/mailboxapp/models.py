from django.db import models
from django.contrib.auth.models import User


class SentEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    from_email = models.EmailField()
    to_email = models.EmailField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} from {self.from_email} to {self.to_email}"


class ReceivedEmail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_emails')
    subject = models.CharField(max_length=255)
    body = models.TextField()
    from_email = models.EmailField()
    to_email = models.EmailField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} from {self.from_email} to {self.to_email}"