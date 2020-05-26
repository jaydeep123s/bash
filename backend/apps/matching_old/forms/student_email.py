from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from apps.matching_old.models import User


class StudentEmailForm(forms.ModelForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ["email"]

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.username = user.email
        user.save()
        return user
