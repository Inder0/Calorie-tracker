from django import forms
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.contrib.auth.models import User

class CustomPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["email"].widget.attrs.update({
            "class": "w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white",
            "placeholder": "Enter your email",
        })

    def clean_email(self):
        email = self.cleaned_data.get("email")
        users = User.objects.filter(email=email)
        if not users.exists():
            return email
        for user in users:
            if not user.has_usable_password():
                raise forms.ValidationError(
                    "This account uses Google login. Please sign in with Google.")
        return email

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'New Password'})
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm New Password'})
    )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full bg-gray-800 border border-gray-700 rounded-xl px-4 py-3 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500",
            })