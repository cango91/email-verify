from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from .email_utils import send_verification_email_wrapper


class EmailVerification(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    email_sent_status = models.BooleanField(default=False)
    last_email_date = models.DateTimeField(null=True)
    verified_date = models.DateTimeField(null=True)
    
    def send_email(self,request=None,domain=None):
        send_verification_email_wrapper(self.user,request,domain)