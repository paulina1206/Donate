from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Name')
    last_name = forms.CharField(label='Surname')
    email = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")

    error_messages = {
        'email_exist': ('User already exists'),
    }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        e = User.objects.filter(email=email)
        if e.count():
            raise forms.ValidationError(
                self.error_messages['email_exist'],
                code='email_exist',
            )
        return email

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
        return user


class DataChangeForm(forms.Form):
    error_messages = {
        'email_inuse': ("This e-mail address cannot be used. Please select a different e-mail address."),
        'password_incorrect': ("Incorrect password."),
    }

    new_first_name = forms.CharField(label='Name')
    new_last_name = forms.CharField(label='Surname')
    new_email = forms.EmailField(
        label=("New E-mail Address"),
        max_length=254,
    )
    current_password = forms.CharField(
        label=("Current Password"),
        widget=forms.PasswordInput,
        required=True
    )


    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(DataChangeForm, self).__init__(*args, **kwargs)

    def clean_current_password(self):
        """
        Validates that the password field is correct.
        """
        current_password = self.cleaned_data["current_password"]
        if not self.user.check_password(current_password):
            raise forms.ValidationError(self.error_messages['password_incorrect'], code='password_incorrect',)
        return current_password

    def clean_new_email1(self):
        """
        Prevents an e-mail address that is already registered from being registered by a different user.
        """
        email = self.cleaned_data.get('new_email')
        if User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError(self.error_messages['email_inuse'], code='email_inuse',)
        return email

    def save(self, commit=True):
        self.user.email = self.cleaned_data['new_email']
        self.user.username = self.cleaned_data["new_email"]
        self.user.first_name = self.cleaned_data["new_first_name"]
        self.user.last_name = self.cleaned_data["new_last_name"]
        if commit:
            self.user.save()
        return self.user