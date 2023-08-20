# import os
# import environ
# from django.test import TestCase
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from .models import EmailVerification
# from .forms import EmailVerificationUserCreationForm

# ## for custom user testing create custom_user app and define custom user model in its models.py
# ## make sure to install it before email_verify

# def simulate_email_send(user, link):
#     print(f"mail sent to {user.email} with link: {link}")
    
# ### PASSED ###
# class EmailVerificationTestCase(TestCase):
#     def setUp(self):
#         settings.EMAIL_VERIFY_SEND_FUNC = simulate_email_send
#         User = get_user_model()
#         self.user = User.objects.create_user('testUser','test@example.com', 'testpassword')
        
#     def test_email_verification_creation(self):
#         # Test that EmailVerification object is created for the user
#         email_verification = EmailVerification.objects.get(user=self.user)
#         self.assertIsNotNone(email_verification)
#         self.assertFalse(email_verification.is_verified)

#     def test_simulated_email_send(self):
#         # Test that the simulated email send function works
#         email_verification = EmailVerification.objects.get(user=self.user)
#         email_verification.send_email()  # This should print the simulated email message

#     def test_user_creation_form(self):
#         # Test the custom user creation form
#         form_data = {'email': 'newuser@example.com', 'password1': 'testpass123', 'password2': 'testpass123'}
#         form = EmailVerificationUserCreationForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         user = form.save()
#         self.assertIsNotNone(user)
#         self.assertEqual(user.email, 'newuser@example.com')

# ### PASSED ###    
# class EmailVerificationSMTPTestCase(TestCase):
#     def setUp(self):
#         environ.Env()
#         environ.Env.read_env()
        
#         settings.DEBUG = True
#         settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#         settings.EMAIL_HOST = os.environ.get('EMAIL_HOST')
#         settings.EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
#         settings.EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
#         settings.EMAIL_PORT = 587
#         settings.EMAIL_USE_TLS = True
#         settings.EMAIL_VERIFY_FROM_ADDRESS = os.environ.get('EMAIL_VERIFY_FROM_ADDRESS')
#         User = get_user_model()
#         self.user = User.objects.create_user('newUser',os.environ.get('EMAIL_VERIFY_FROM_ADDRESS'), 'testpassword')
#     def test_email_verification_creation(self):
#         # Test that EmailVerification object is created for the user
#         email_verification = EmailVerification.objects.get(user=self.user)
#         self.assertIsNotNone(email_verification)
#         self.assertFalse(email_verification.is_verified)
        
#     def test_user_creation_form(self):
#         # Test the custom user creation form
#         form_data = {'email': os.environ.get('EMAIL_VERIFY_FROM_ADDRESS'), 'password1': 'testpass123', 'password2': 'testpass123'}
#         form = EmailVerificationUserCreationForm(data=form_data)
#         self.assertTrue(form.is_valid())
#         user = form.save()
#         self.assertIsNotNone(user)
#         self.assertEqual(user.email, os.environ.get('EMAIL_VERIFY_FROM_ADDRESS'))