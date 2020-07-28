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
