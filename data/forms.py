from django import forms
from .validators import validate_file_extension
from .models import Document


# class UploadFileForm(forms.Form):
#     file = forms.FileField(validators=[validate_file_extension])
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['file'].label = "File"
#         self.fields['file'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload File'})


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['document_title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Document Tit'})
        self.fields['resource_url'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Document Source Url'})
        self.fields['author_name'].widget.attrs.update({'class': 'form-control', })
        self.fields['published_year'].widget.attrs.update({'class': 'form-control', })
        self.fields['description'].widget.attrs.update({'class': 'form-control', })
        self.fields['number_of_pages'].widget.attrs.update({'class': 'form-control', })
        self.fields['file'].widget.attrs.update({'class': 'form-control', })
