from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django.db.models import Model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    online_id = forms.CharField(
        required=True,
        label="online id"
    )

    class Meta:
        model = User
        fields = (
            "username",
            "online_id",
            "password1",
            "password2"
        )