from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from anymail.signals import inbound
from django.dispatch import receiver
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SentEmail, ReceivedEmail
from .serializers import SentEmailSerializer, ReceivedEmailSerializer
import logging
from rest_framework import serializers 
from rest_framework.permissions import IsAuthenticated
logger = logging.getLogger(__name__)

# https://KOUK4706nKbIEChc:sq7ImdYBScBHsaUS@late-plums-juggle.loca.lt/anymail/mailgun/inbound/v
# Webhook for receiving emails
@receiver(inbound)
def handle_inbound_email(sender, event, esp_name, **kwargs):
    message = event.message
    recipient = message.envelope_recipient  # e.g., smit.vekariya@sandbox123abc.mailgun.org
    print("recipient", recipient)
    username = recipient.split('@')[0]
    print("username", username)
    try:
        user = User.objects.get(username=username)
        ReceivedEmail.objects.create(
            user=user,
            subject=message.subject or '(No subject)',
            body=message.text or message.html or '',
            from_email=message.from_email,
            to_email=recipient,
            received_at=message.date or timezone.now()
        )
        logger.info(f"Email received for {recipient}")
    except User.DoesNotExist:
        logger.error(f"No user found for {recipient}")
    except Exception as e:
        logger.error(f"Error processing email for {recipient}: {str(e)}")

# https://late-plums-juggle.loca.lt/mailbox/webhook/

@csrf_exempt
def webhook(request):
    # signature = request.POST["signature"]
    # print("signature", signature)
    # sender = request.POST["sender"]
    # print("sender", sender)
    # subject = request.POST["subject"]
    # print("subject", subject)
    # recipient = request.POST["recipient"]
    # print("recipient", recipient)
    # Body_plain = request.POST["body-plain"]
    # print("Body_plain", Body_plain)
    print(f"Webhook received: {request.method}")
    return HttpResponse(status=200)

# Web views
@login_required
def send_email(request):
    user_email = f"{request.user.username}@{settings.ANYMAIL['MAILGUN_SENDER_DOMAIN']}"
    if request.method == 'POST':
        to_email = request.POST.get('to_email')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        try:
            send_mail(
                subject=subject,
                message=body,
                from_email=user_email,
                recipient_list=[to_email],
                fail_silently=False,
            )
            SentEmail.objects.create(
                user=request.user,
                subject=subject,
                body=body,
                from_email=user_email,
                to_email=to_email
            )
            return redirect('inbox')
        except Exception as e:
            logger.error(f"Error sending email from {user_email}: {str(e)}")
            return render(request, 'send_email.html', {'error': str(e)})
    return render(request, 'send_email.html', {'user_email': user_email})


@login_required
def inbox(request):
    received_emails = ReceivedEmail.objects.filter(user=request.user).order_by('-received_at')
    sent_emails = SentEmail.objects.filter(user=request.user).order_by('-sent_at')
    return render(request, 'inbox.html', {
        'received_emails': received_emails,
        'sent_emails': sent_emails,
        'user_email': f"{request.user.username}@{settings.ANYMAIL['MAILGUN_SENDER_DOMAIN']}"
    })


# API views
class SentEmailViewSet(viewsets.ModelViewSet):
    serializer_class = SentEmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SentEmail.objects.filter(user=self.request.user).order_by('-sent_at')

    def perform_create(self, serializer):
        user_email = f"{self.request.user.username}@{settings.ANYMAIL['MAILGUN_SENDER_DOMAIN']}"
        try:
            send_mail(
                subject=serializer.validated_data['subject'],
                message=serializer.validated_data['body'],
                from_email=user_email,
                recipient_list=[serializer.validated_data['to_email']],
                fail_silently=False,
            )
            serializer.save(user=self.request.user, from_email=user_email)
        except Exception as e:
            logger.error(f"Error sending email from {user_email}: {str(e)}")
            raise serializers.ValidationError(f"Failed to send email: {str(e)}")

class ReceivedEmailViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ReceivedEmailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ReceivedEmail.objects.filter(user=self.request.user).order_by('-received_at')