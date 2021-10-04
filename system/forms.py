from django import forms
from system.models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('to_user', 'from_user', 'message')
        widgets = {
            'to_user' : forms.HiddenInput(),
            'from_user' : forms.HiddenInput(),
        }
