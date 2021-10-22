from django import forms
from .models import Conversation


class ConversationForm(forms.ModelForm):
    class Meta:
        model = Conversation
        fields = ('name', 'bot')
        # widgets = {'slug': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Conversation Name"
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Conversation Name'})
        self.fields['bot'].widget.attrs.update({'class': 'form-control'})
        # self.fields['user'].widget = forms.HiddenInput()
