from django import forms
from .validators import validate_file_extension


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_extension])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['file'].label = "File"
        self.fields['file'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload File'})

