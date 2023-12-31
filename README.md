# email-verify
See it on: [GitHub](https://github.com/cango91/email-verify) | [PyPI](https://pypi.org/project/email-verify/)


A lightweight Django app for adding user email verification at registration.
## contents
+ [features](#features)
+ [setup](#setup)
+ [usage](#usage)
+ [mixin and decorator](#mixin-and-decorator)
+ [custom redirections and template overriding](#custom-redirections-and-template-overriding)
+ [custom email subject, body and sender](#cutom-email-subject-body-and-sender)
+ [providing the domain to the email function](#providing-the-domain-to-the-email-function)
  + [known issue with domain retrieval](#known-issue-with-domain-retrieval)


+ [changelog:](#changelog)
  + [v0.1.5](#v015)
  + [v0.1.4](#v014)
  + [v0.1.3](#v013)
  + [v0.1.2](#v012)
  + [v0.1.1](#v011)

## features
+ Easy integration with any Django app
+ Designed the Django way - offers granular customization alongside default behavior
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
# settings.py:

INSTALLED_APPS = [
    'your_main_app',
    'email_verify',
    'django.contrib.admin',
    # ...
]
```

Include the url conf of email-verify in your project's (not your app's) url configuration, after your other url confs. 

```py
# urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('your/main/app.urls')),
    # ...
    path('where/you/want/', include('email_verify.urls')),
]

```

Once you add the app to your INSTALLED_APPS, you might notice you have a new migration available. email-verify establishes a one-to-one relation with the built-in User model (from django.contrib.auth.models).

You can apply migrations via:

`python manage.py migrate`

**Setting up default send function:**

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

**Providing a custom send function:**

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

### usage

email-verify creates a one-to-one relation with the built-in User model. Every time a new User is created and saved, email-verify will create a new EmailVerification record with is_verified set to false. On its own this has no effect on your project, except modifying your User model with an EmailVerification relation.

If you're using `UserCreationForm` you can instead use `EmailValidationUserCreation` for exposing email on sign-up. If `EMAIL_VERIFY_ENFORCE_UNIQUE_EMAILS` is `True` (default) a signal will trigger pre_save, and will throw a `django.core.exceptions.ValidationError`. This will not be handled by the Form, as it only checks for email validity and non-emptiness.

If your SMTP configuration or custom emailing function is setup correctly, an email message will be delivered to the address used at registration as soon as a user registers. Lookout for custom `EmailSendingException` on user.save(). No silent errors.

By default the following urlpattern will be used for the verification endpoint: `verify_email/<str:token>/`

If you want to use another endpoint for verification, be sure to set it up in your projects's url conf before including email_verify's url conf. Customized url pattern must have a `<str:token>`.

<blockquote>
The token is cryptographically signed using `itsdangerous` package. Message includes the user's id, current domain/host and a timestamp. The domain is not used for verification if `DEBUG=True` in `settings.py`, but in production, it checks against `ALLOWED_HOSTS` and will reject the token if the domain value is not found within the list. The timestamp is used to check against `EMAIL_VERIFY_EXPIRES_IN` (defaults to 3600 seconds) value to consider the token expired. If this value is not positive, the token won't expire.
</blockquote>

#### mixin and decorator
To restrict access to unverified users, you may decorate your view functions with `@user_verified` from `email_verify.decorators`, or you may use `EmailVerificationMixin` from `email_verify.mixins` for your class-based views. In either case, `is_authenticated` is checked internally, so you wouldn't need `@require_login` or `LoginRequiredMixin` on-top.

#### custom redirections and template overriding
There are several ways you can customize `email-verify`. You can bypass all view functionality by urlconf, as all logic is handled by signals during `.save()` calls. You can provide redirect urls to `EmailVerificationView` for `success_url` and `failure_url`, or you can overwrite the default templates at `templates/email_verify/success.html` and `templates/email_verify/failure.html`. For failure rendering, `EmailVerificationView` will provide an error message in context: `message`. For success rendering, it will provide a `main_page` which can be provided via `MAIN_PAGE` in settings.py (default `'/'`) which will provide a link to your home page for the default success template.


#### custom email subject, body and sender

Customize your subject field by providing `EMAIL_VERIFY_SUBJECT_LINE` in settings.py
You can also customize the body of your email. Be sure to:
+ Include the verification link via `$:_VERIFICATION_LINK` magic string somewhere
+ If you provide `EMAIL_VERIFY_HTML_MESSAGE` also provide `EMAIL_VERIFY_TEXT_MESSAGE` as a fallback.
You can change the sender email via `EMAIL_VERIFY_FROM_ADDRESS`

#### providing the domain to the email function
The function(s) used for sending emails can be accessed at `email_verify.email_utils`. You may want to use these functions manually in your workflow. `send_verification_email(user, send_email_func, request=None)` requires the current domain to be signed with the token and will try to retrieve it using the following code-block. Depending on where you call this function, you may want to pass a `request` object to it. Explicit passing of a domain/host name was abandoned in favor of user-friendliness (optional `domain` keyword is added in 0.1.5, which will bypass the following code block if provided):
```py
 # Use the request object if provided, otherwise fall back to ALLOWED_HOSTS
    if request:
        current_site = get_current_site(request)
        domain = current_site.domain
        port = request.get_port()
        if port not in ('80', '443'):
            domain += f":{port}"
    else:
        if settings.DEBUG:
            domain = settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'
            domain = 'localhost' if domain == '*' else domain
            port = settings.DEBUG_PORT if hasattr(settings, 'DEBUG_PORT') else '8000'
            domain += f":{port}"
        elif settings.ALLOWED_HOSTS:
            domain = settings.ALLOWED_HOSTS[0]
        else:
            raise InvalidDomainException("Couldn't resolve domain for token. If DEBUG is set to False ALLOWED_HOSTS[0] must be set or request object should be passed to function send_verification_email")
```
Be sure to set a `DEBUG_PORT` during development if you're using another port than `8000` (i.e. running multiple Django servers). 

If you're using non-http and non-https ports in production, in order for a valid verification URL to be generated you should either pass in a `request` object, or a `domain` string with `domain:port` formatting.


##### known issue with domain retrieval:
If you're using `django_on_heroku`, the `ALLOWED_HOSTS=['*']` overwrite is breaking. You can either disable the allowed_hosts modification of `django_on_heroku` or (added in 0.1.6) provide a host via `EMAIL_VERIFY_ALLOWED_HOST` literal in `settings.py` which `email_verify.utils.verify_token` will use to check against the unsigned token's domain. You will still have to provide a request object or a domain string to the downstream functions to correctly get a domain for signing. You can provide a string in `EMAIL_VERIFY_USE_DOMAIN` literal to coerce internal functions to use the given domain. This will take precedence over all other methods except providing a domain to the functions directly.

## Changelog
### v0.1.10 (hotfix)
+ Broken username fix
### v0.1.9 (hotfix)
+ Broken domain verification logic fix
### v0.1.8 (hotfix)
+ 0.1.7 did not work as intended
### v0.1.7 (hotfix)
+ If username field exists, set ordering to show it on top.
### v0.1.6
+ Decouple logic from built-in User model. Instead of `User` use `get_user_model()` for cases where a custom user model is used.
+ Add a workaround for `ALLOWED_HOSTS` * overwrites. Introduced `EMAIL_VERIFY_ALLOWED_HOST` and `EMAIL_VERIFY_USE_DOMAIN`
+ Add `tests.py`
+ `EmailVerificationUserCreationForm` now only exposes `email` field. Checks if the `AUTH_USER_MODEL` has a username field before attempting to expose it.
### v0.1.5
+ Documentation update
+ Added `domain` as an optional argument to `send_verification_email` and its wrappers for bypassing domain retrieval logic and providing the domain directly.
### v0.1.4
+ Feature: If existing users without e-mails access a `@user_verified` decorated view or `UserVerifiedMixin` CBV, they will get a 404 instead of rising an error.
### v0.1.3
+ Add `UserVerifiedMixin`
### v0.1.2 (hotfix)
+ Bugfix: e-mail uniqueness not enforced if email is empty
### v0.1.1
+ Introduced email uniqueness enforcing
+ Decoupled emailing logic from Form and Views, email is sent via Signal receiver at time of creation
+ Enhanced model:
   + Removed `verified_by_admin`
   + Added `email_sent_status`, `last_email_date`, `verified_date` fields
+ Removed admin site registration
+ Custom form no longer redirects
+ Removed ***_TEMPLATE_NAME pattern
+ Removed templates, urlconfs and views pertaining to email sending status
+ Added `EmailSendingException` which can be used to handle email sending status by the user
+ Converted `email_verify:verify_email` to CBV. Uses success and failure redirections with failure message as query parameter.
+ Removed `is_valid` overwrite to use `clean_email`, in-line with Django's built-in validation mechanisms.