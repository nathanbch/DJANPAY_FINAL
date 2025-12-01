from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'consent']


class TransferForm(forms.Form):
    receiver_username = forms.CharField(
        label="Nom d'utilisateur du destinataire",
        max_length=150
    )
    amount = forms.DecimalField(
        label="Montant",
        max_digits=10,
        decimal_places=2,
        min_value=0.01
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)

    def clean_receiver_username(self):
        username = self.cleaned_data["receiver_username"]

        if username == self.user.username:
            raise ValidationError("Vous ne pouvez pas vous envoyer de l'argent à vous-même.")

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError("Aucun utilisateur avec ce nom d'utilisateur.")

        return username
