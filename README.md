# email-verify 0.1
A Django app for adding user email verification at registration.

## features
+ Easy integration with any Django app
+ Designed the Django way - highly opinionated, offers granular customization alongside default behavior
+ Works out-of-the-box with Django's SMTP backend. Can be customized to work with any backend.

## getting started
### setup
Install it with:

 `pip install email-verify`

<blockquote>
If you're using virtual environments, make sure to activate it before running this command
</blockquote>
<br>

Add `email_verify` to your `INSTALLED_APPS` list, after your main app. Your INSTALLED_APPS should look similar to this:
```py
INSTALLED_APPS = [
    'your_main_app',
    'email_verify',
    'django.contrib.admin',
    # ...
]
```

**Setting up defaults:**

email-verify is designed work out-of-the-box with Django's SMTP backend. If you want to keep to defaults, make sure to add the following configuration to your settings (assuming the hostname, host user and password are kept in environment variables):
```py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = 587 # or any other SMTP port your host is configured towards
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True # or False, depending on your host configuration

```

The above is the standard configuration for Django's SMTP backend.

If you don't want to use Django's default SMTP backend or have a specific function you'd rather use, provide the function in `EMAIL_VERIFY_SEND_FUNC` in your `settings.py`. The function provided should accept 2 arguments: user and verification_link. You can access user's e-mail through `user.email`.

Below is an example for a custom emailing function. In this example, instead of actually sending an email, we print the token on the console (useful during dev):

```py
# custom email function example:
# define a custom function
def custom_send_email(user,verification_link):
    print(verification_link)

# settings.py
# set EMAIL_VERIFY_SEND_FUNC to your custom function
EMAIL_VERIFY_SEND_FUNC = custom_send_email
```

