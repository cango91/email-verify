from collections import OrderedDict
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator

class EmailVerificationUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        User = get_user_model()
        if 'username' in [field.name for field in User._meta.fields]:
            self.fields['username'] = forms.CharField(max_length=30)
            new_order = OrderedDict()
            new_order['username'] = self.fields['username']
            for key, value in self.fields.items():
                if key != 'username':
                    new_order[key] = value
            self.fields = new_order

    def clean_email(self):
        email = self.cleaned_data.get('email', None)
        if email:
            try:
                EmailValidator(message="Invalid e-mail")(email)
            except ValidationError as e:
                raise ValidationError("Invalid e-mail")
        return email

    def save(self, commit=True, request=None):
        user = super().save(commit=False)
        username_field_name = 'username'
        if username_field_name in self.cleaned_data:
            setattr(user, username_field_name, self.cleaned_data[username_field_name])
        if commit:
            user.save()
        return user